import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from winforge.models.system import SystemHealthReport, OSInfo, PowerPlan
from winforge.models.policy import DeviceProfile, PolicyRule
from winforge.models.tweak import Tweak, TweakCategory
from winforge.utils.paths import get_config_dir

logger = logging.getLogger("winforge")


class PolicyEngine:
    """Evaluates system context against safety rules and Windows compatibility matrix."""

    def __init__(self):
        self.compat_matrix: Dict[str, Any] = self._load_compatibility_matrix()

    def _load_compatibility_matrix(self) -> Dict[str, Any]:
        """Loads config/windows_compatibility.json."""
        matrix_file = get_config_dir() / "windows_compatibility.json"
        if matrix_file.exists():
            try:
                with open(matrix_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed loading compatibility matrix: {e}")
        return {"forbidden_tweaks_all_versions": ["DISABLE_DEFENDER", "PERMANENT_DISABLE_WINDOWS_UPDATE"]}

    def build_device_profile(self, report: SystemHealthReport) -> DeviceProfile:
        """Constructs a DeviceProfile from system health report."""
        build_num = 22621
        try:
            build_num = int(report.os.build_number.split(".")[0])
        except Exception:
            pass

        is_server = "Server" in report.os.product_name
        is_laptop = report.power.is_on_battery or any("battery" in d.drive_letter.lower() for d in report.drives)

        return DeviceProfile(
            is_laptop=is_laptop,
            is_server=is_server,
            is_domain_joined=report.os.is_domain_joined,
            is_on_battery=report.power.is_on_battery,
            os_build=build_num,
            total_ram_gb=report.ram.total_gb
        )

    def evaluate_tweak(self, tweak: Tweak, profile: DeviceProfile) -> PolicyRule:
        """Evaluates whether a specific tweak is permitted for the given device profile."""
        # 1. Non-negotiable forbidden tweaks check
        forbidden_list = self.compat_matrix.get("forbidden_tweaks_all_versions", [])
        if tweak.id.upper() in forbidden_list or "DEFENDER" in tweak.id.upper() or "UPDATE" in tweak.id.upper():
            return PolicyRule(
                rule_id=tweak.id,
                description=tweak.name,
                allowed=False,
                reason="BLOCKED: Tweak violates core non-negotiable security guardrails (Defender/Windows Update/System files)."
            )

        # 2. Server OS checks
        if profile.is_server:
            if tweak.category == TweakCategory.GAMING:
                return PolicyRule(
                    rule_id=tweak.id,
                    description=tweak.name,
                    allowed=False,
                    reason="BLOCKED: Gaming tweaks are disabled on Windows Server OS to preserve server workload stability."
                )

        # 3. Battery / Laptop checks
        if profile.is_on_battery:
            if tweak.category == TweakCategory.POWER:
                return PolicyRule(
                    rule_id=tweak.id,
                    description=tweak.name,
                    allowed=False,
                    reason="BLOCKED: Aggressive power plan modifications are restricted while running on battery power."
                )

        # 4. Domain-Joined Enterprise checks
        if profile.is_domain_joined:
            if tweak.category == TweakCategory.NETWORK or "GPO" in tweak.description.upper():
                return PolicyRule(
                    rule_id=tweak.id,
                    description=tweak.name,
                    allowed=False,
                    reason="BLOCKED: Network/GPO tweaks are restricted on Domain-Joined machines to preserve enterprise policy."
                )

        return PolicyRule(
            rule_id=tweak.id,
            description=tweak.name,
            allowed=True,
            reason="ALLOWED: Tweak satisfies all safety policy rules and compatibility checks."
        )
