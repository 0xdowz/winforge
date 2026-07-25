from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any
from pathlib import Path

from winforge.models.system import SystemHealthReport
from winforge.models.tweak import Tweak


class BaseOptimizer(ABC):
    """Abstract Base Class for Category Optimizers."""

    @abstractmethod
    def detect(self, report: SystemHealthReport) -> List[Tweak]:
        """Detect applicable tweaks for the given diagnostic report."""
        pass

    @abstractmethod
    def apply_tweak(self, tweak: Tweak, mock: bool = True) -> Tuple[bool, str]:
        """Apply tweak modifications (mock=True for safe execution)."""
        pass

    @abstractmethod
    def verify_tweak(self, tweak: Tweak, mock: bool = True) -> Tuple[bool, str]:
        """Verify tweak modifications post-apply."""
        pass

    @abstractmethod
    def rollback(self, tweak: Tweak, session_dir: Path) -> Tuple[bool, str]:
        """Revert tweak modifications to pre-execution state."""
        pass
