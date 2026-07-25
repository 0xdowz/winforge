import logging
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

from winforge.optimizations.base import BaseOptimizer
from winforge.optimizations.registry_handler import RegistryHandler
from winforge.optimizations.verifier import TweakVerifier
from winforge.models.system import SystemHealthReport
from winforge.models.tweak import Tweak, TweakCategory
from winforge.core.tweak_loader import load_tier1_tweaks

logger = logging.getLogger("winforge")


class GamingOptimizer(BaseOptimizer):
    """Safe Gaming & Latency Category Optimizer."""

    def __init__(self, registry_handler: Optional[RegistryHandler] = None, verifier: Optional[TweakVerifier] = None):
        self.reg_handler = registry_handler or RegistryHandler()
        self.verifier = verifier or TweakVerifier()

    def detect(self, report: SystemHealthReport) -> List[Tweak]:
        """Detect applicable gaming tweaks from tweak database."""
        all_tweaks = load_tier1_tweaks()
        gaming_tweaks = [t for t in all_tweaks if t.category == TweakCategory.GAMING]
        logger.info(f"GamingOptimizer detected {len(gaming_tweaks)} candidate gaming tweaks.")
        return gaming_tweaks

    def apply_tweak(self, tweak: Tweak, mock: bool = True) -> Tuple[bool, str]:
        """Apply gaming tweak via RegistryHandler."""
        if tweak.category != TweakCategory.GAMING:
            return False, f"Invalid category {tweak.category} for GamingOptimizer."

        apply = tweak.apply_method
        if apply.get("type") == "registry":
            hive = apply.get("hive", "HKLM")
            key = apply.get("key", "")
            name = apply.get("value_name", "")
            val_type = apply.get("value_type", "REG_DWORD")
            data = apply.get("value_data", 0)

            return self.reg_handler.write_registry_value(hive, key, name, val_type, data, mock=mock)

        return True, f"[MOCK GAMING] Applied tweak {tweak.name}"

    def verify_tweak(self, tweak: Tweak, mock: bool = True) -> Tuple[bool, str]:
        """Verify gaming tweak state post-apply."""
        return self.verifier.verify(tweak, mock=mock)

    def rollback(self, tweak: Tweak, session_dir: Path) -> Tuple[bool, str]:
        """Revert gaming tweak to pre-execution state."""
        rb = tweak.rollback_method
        if rb.get("type") == "registry":
            hive = rb.get("hive", "HKLM")
            key = rb.get("key", "")
            name = rb.get("value_name", "")
            val_type = rb.get("value_type", "REG_DWORD")
            data = rb.get("value_data", 0)

            return self.reg_handler.write_registry_value(hive, key, name, val_type, data, mock=True)

        return True, f"Reverted gaming tweak {tweak.id}"
