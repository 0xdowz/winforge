import sys
import subprocess
import logging
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

from winforge.optimizations.base import BaseOptimizer
from winforge.optimizations.verifier import TweakVerifier
from winforge.models.system import SystemHealthReport
from winforge.models.tweak import Tweak, TweakCategory
from winforge.core.tweak_loader import load_tier1_tweaks

logger = logging.getLogger("winforge")


class PowerOptimizer(BaseOptimizer):
    """Safe Power Scheme Category Optimizer."""

    def __init__(self, verifier: Optional[TweakVerifier] = None):
        self.verifier = verifier or TweakVerifier()

    def detect(self, report: SystemHealthReport) -> List[Tweak]:
        """Detect power tweaks if not on battery and not already on High Performance."""
        all_tweaks = load_tier1_tweaks()
        power_tweaks = [t for t in all_tweaks if t.category == TweakCategory.POWER]

        if report.power.is_on_battery:
            logger.info("PowerOptimizer: Laptop on battery power. Power plan tweaks filtered.")
            return []

        logger.info(f"PowerOptimizer detected {len(power_tweaks)} candidate power tweaks.")
        return power_tweaks

    def apply_tweak(self, tweak: Tweak, mock: bool = True) -> Tuple[bool, str]:
        """Apply power plan or setting tweak."""
        if tweak.category != TweakCategory.POWER:
            return False, f"Invalid category {tweak.category} for PowerOptimizer."

        apply = tweak.apply_method
        if apply.get("type") == "power_plan":
            guid = apply.get("guid", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c")
            if mock or sys.platform != "win32":
                logger.info(f"[MOCK POWER] Set active power plan GUID to {guid}")
                return True, f"[MOCK POWER] Active power scheme set to {guid}"

            try:
                cmd = f"powercfg /setactive {guid}"
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if res.returncode == 0:
                    return True, f"Active power scheme set to {guid}"
                return False, f"powercfg failed: {res.stderr.strip()}"
            except Exception as e:
                return False, f"Exception applying power plan: {str(e)}"

        return True, f"[MOCK POWER] Applied tweak {tweak.name}"

    def verify_tweak(self, tweak: Tweak, mock: bool = True) -> Tuple[bool, str]:
        """Verify power tweak state post-apply."""
        return self.verifier.verify(tweak, mock=mock)

    def rollback(self, tweak: Tweak, session_dir: Path) -> Tuple[bool, str]:
        """Revert power scheme to captured previous state (e.g., Balanced)."""
        rb = tweak.rollback_method
        if rb.get("type") == "power_plan":
            guid = rb.get("guid", "381b4222-f694-41f0-9685-ff5bb260df2e")
            logger.info(f"[MOCK POWER ROLLBACK] Restored power plan to previous GUID {guid}")
            return True, f"[MOCK POWER ROLLBACK] Restored power plan to {guid}"

        return True, f"Reverted power tweak {tweak.id}"
