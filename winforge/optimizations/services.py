import logging
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

from winforge.optimizations.base import BaseOptimizer
from winforge.optimizations.service_handler import ServiceHandler
from winforge.optimizations.verifier import TweakVerifier
from winforge.models.system import SystemHealthReport
from winforge.models.tweak import Tweak, TweakCategory
from winforge.analyzers.services import CRITICAL_SERVICES
from winforge.core.tweak_loader import load_tier1_tweaks

logger = logging.getLogger("winforge")

# Strict immutable list of protected system services that must NEVER be modified
IMMUTABLE_PROTECTED_SERVICES = CRITICAL_SERVICES.union({
    "rpcss", "dcomlaunch", "eventlog", "plugplay", "cryptsvc",
    "dhcp", "dnscache", "lsass", "windefend", "wdnissvc",
    "sense", "wuauserv", "samss", "gpsvc", "seclogon", "lanmanserver", "lanmanworkstation"
})


class ServicesOptimizer(BaseOptimizer):
    """Safe Windows Service Hygiene Category Optimizer."""

    def __init__(
        self,
        service_handler: Optional[ServiceHandler] = None,
        verifier: Optional[TweakVerifier] = None
    ):
        self.svc_handler = service_handler or ServiceHandler()
        self.verifier = verifier or TweakVerifier()

    def detect(self, report: SystemHealthReport) -> List[Tweak]:
        """Detect safe service tweaks from tweak database while guaranteeing protection of critical services."""
        all_tweaks = load_tier1_tweaks()
        service_tweaks = [t for t in all_tweaks if t.category in (TweakCategory.SERVICES, TweakCategory.STARTUP, TweakCategory.SECURITY_PRIVACY)]

        safe_tweaks: List[Tweak] = []
        for t in service_tweaks:
            target_svc = t.apply_method.get("service_name", "").lower()
            if target_svc in IMMUTABLE_PROTECTED_SERVICES:
                logger.error(f"SECURITY VIOLATION BLOCKED: Attempted to configure protected service {target_svc} in tweak {t.id}")
                continue
            if target_svc:
                safe_tweaks.append(t)

        logger.info(f"ServicesOptimizer detected {len(safe_tweaks)} safe candidate service tweaks.")
        return safe_tweaks

    def apply_tweak(self, tweak: Tweak, mock: bool = True) -> Tuple[bool, str]:
        """Apply service startup configuration update via ServiceHandler."""
        svc_name = tweak.apply_method.get("service_name", "").lower()
        if svc_name in IMMUTABLE_PROTECTED_SERVICES:
            return False, f"SECURITY REJECTED: Modification of critical system service '{svc_name}' is strictly prohibited."

        start_type = tweak.apply_method.get("start_type", "demand")
        return self.svc_handler.set_service_start_type(svc_name, start_type, mock=mock)

    def verify_tweak(self, tweak: Tweak, mock: bool = True) -> Tuple[bool, str]:
        """Verify service state post-apply."""
        return self.verifier.verify(tweak, mock=mock)

    def rollback(self, tweak: Tweak, session_dir: Path) -> Tuple[bool, str]:
        """Revert service startup type to pre-execution state."""
        svc_name = tweak.rollback_method.get("service_name", "").lower()
        start_type = tweak.rollback_method.get("start_type", "auto")
        return self.svc_handler.set_service_start_type(svc_name, start_type, mock=True)
