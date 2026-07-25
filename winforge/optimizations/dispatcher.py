import logging
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

from winforge.models.system import SystemHealthReport
from winforge.models.tweak import Tweak, TweakCategory
from winforge.optimizations.base import BaseOptimizer
from winforge.optimizations.gaming import GamingOptimizer
from winforge.optimizations.power import PowerOptimizer
from winforge.optimizations.startup import StartupOptimizer
from winforge.optimizations.services import ServicesOptimizer
from winforge.optimizations.cleanup import CleanupOptimizer
from winforge.optimizations.network import NetworkOptimizer

logger = logging.getLogger("winforge")


class CategoryDispatcher:
    """Category Optimizer Dispatcher that routes tweaks to dedicated category optimizers."""

    def __init__(self):
        self.optimizers: Dict[TweakCategory, BaseOptimizer] = {
            TweakCategory.GAMING: GamingOptimizer(),
            TweakCategory.POWER: PowerOptimizer(),
            TweakCategory.STARTUP: StartupOptimizer(),
            TweakCategory.SERVICES: ServicesOptimizer(),
            TweakCategory.CLEANUP: CleanupOptimizer(),
            TweakCategory.NETWORK: NetworkOptimizer(),
            TweakCategory.SECURITY_PRIVACY: ServicesOptimizer()
        }

    def get_optimizer(self, category: TweakCategory) -> Optional[BaseOptimizer]:
        """Retrieve dedicated category optimizer or None if unsupported."""
        opt = self.optimizers.get(category)
        if not opt:
            logger.warning(f"No registered optimizer found for category {category}")
        return opt

    def detect_all_candidate_tweaks(self, report: SystemHealthReport) -> List[Tweak]:
        """Collect detected tweaks from all registered category optimizers."""
        detected: List[Tweak] = []
        seen_ids = set()

        for cat, opt in self.optimizers.items():
            try:
                tweaks = opt.detect(report)
                for t in tweaks:
                    if t.id not in seen_ids:
                        seen_ids.add(t.id)
                        detected.append(t)
            except Exception as e:
                logger.error(f"Error detecting tweaks for category {cat}: {e}")

        logger.info(f"CategoryDispatcher detected {len(detected)} unique candidate tweaks.")
        return detected

    def apply_tweak(self, tweak: Tweak, mock: bool = True) -> Tuple[bool, str]:
        """Route tweak apply execution to dedicated category optimizer."""
        opt = self.get_optimizer(tweak.category)
        if not opt:
            return False, f"Unsupported category {tweak.category} for tweak {tweak.id}"

        logger.info(f"Dispatching apply for tweak {tweak.id} ({tweak.name}) -> {opt.__class__.__name__}")
        return opt.apply_tweak(tweak, mock=mock)

    def verify_tweak(self, tweak: Tweak, mock: bool = True) -> Tuple[bool, str]:
        """Route tweak verification to dedicated category optimizer."""
        opt = self.get_optimizer(tweak.category)
        if not opt:
            return False, f"Unsupported category {tweak.category} for tweak {tweak.id}"

        return opt.verify_tweak(tweak, mock=mock)

    def rollback_tweak(self, tweak: Tweak, session_dir: Path) -> Tuple[bool, str]:
        """Route tweak rollback to dedicated category optimizer."""
        opt = self.get_optimizer(tweak.category)
        if not opt:
            return False, f"Unsupported category {tweak.category} for tweak {tweak.id}"

        return opt.rollback(tweak, session_dir)
