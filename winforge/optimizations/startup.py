import logging
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

from winforge.optimizations.base import BaseOptimizer
from winforge.optimizations.registry_handler import RegistryHandler
from winforge.optimizations.service_handler import ServiceHandler
from winforge.optimizations.verifier import TweakVerifier
from winforge.models.system import SystemHealthReport
from winforge.models.tweak import Tweak, TweakCategory
from winforge.core.tweak_loader import load_tier1_tweaks

logger = logging.getLogger("winforge")

# Strict list of protected startup keywords that must NEVER be modified
PROTECTED_STARTUP_KEYWORDS = {
    "windefend", "defender", "antivirus", "security", "driver",
    "intel", "amd", "nvidia", "realtek", "audio", "display"
}


class StartupOptimizer(BaseOptimizer):
    """Safe Startup Hygiene Category Optimizer."""

    def __init__(
        self,
        registry_handler: Optional[RegistryHandler] = None,
        service_handler: Optional[ServiceHandler] = None,
        verifier: Optional[TweakVerifier] = None
    ):
        self.reg_handler = registry_handler or RegistryHandler()
        self.svc_handler = service_handler or ServiceHandler()
        self.verifier = verifier or TweakVerifier()

    def detect(self, report: SystemHealthReport) -> List[Tweak]:
        """Detect applicable startup tweaks from tweak database."""
        all_tweaks = load_tier1_tweaks()
        startup_tweaks = [t for t in all_tweaks if t.category == TweakCategory.STARTUP]

        # Filter out any protected keywords
        safe_tweaks = []
        for t in startup_tweaks:
            name_lower = t.name.lower()
            if any(k in name_lower for k in PROTECTED_STARTUP_KEYWORDS):
                logger.warning(f"StartupOptimizer: Skipping protected startup item {t.name}")
                continue
            safe_tweaks.append(t)

        logger.info(f"StartupOptimizer detected {len(safe_tweaks)} safe candidate startup tweaks.")
        return safe_tweaks

    def apply_tweak(self, tweak: Tweak, mock: bool = True) -> Tuple[bool, str]:
        """Apply startup tweak via RegistryHandler or ServiceHandler."""
        if tweak.category != TweakCategory.STARTUP and tweak.category != TweakCategory.SECURITY_PRIVACY:
            return False, f"Invalid category {tweak.category} for StartupOptimizer."

        apply = tweak.apply_method
        method_type = apply.get("type")

        if method_type == "registry":
            hive = apply.get("hive", "HKLM")
            key = apply.get("key", "")
            name = apply.get("value_name", "")
            val_type = apply.get("value_type", "REG_DWORD")
            data = apply.get("value_data", 0)
            return self.reg_handler.write_registry_value(hive, key, name, val_type, data, mock=mock)

        elif method_type == "service":
            svc_name = apply.get("service_name", "")
            start_type = apply.get("start_type", "demand")
            return self.svc_handler.set_service_start_type(svc_name, start_type, mock=mock)

        return True, f"[MOCK STARTUP] Applied tweak {tweak.name}"

    def verify_tweak(self, tweak: Tweak, mock: bool = True) -> Tuple[bool, str]:
        """Verify startup tweak state post-apply."""
        return self.verifier.verify(tweak, mock=mock)

    def rollback(self, tweak: Tweak, session_dir: Path) -> Tuple[bool, str]:
        """Revert startup tweak to pre-execution state."""
        rb = tweak.rollback_method
        method_type = rb.get("type")

        if method_type == "registry":
            hive = rb.get("hive", "HKLM")
            key = rb.get("key", "")
            name = rb.get("value_name", "")
            val_type = rb.get("value_type", "REG_DWORD")
            data = rb.get("value_data", 0)
            return self.reg_handler.write_registry_value(hive, key, name, val_type, data, mock=True)

        elif method_type == "service":
            svc_name = rb.get("service_name", "")
            start_type = rb.get("start_type", "auto")
            return self.svc_handler.set_service_start_type(svc_name, start_type, mock=True)

        return True, f"Reverted startup tweak {tweak.id}"
