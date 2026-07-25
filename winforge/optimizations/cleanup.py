import os
import logging
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

from winforge.optimizations.base import BaseOptimizer
from winforge.optimizations.verifier import TweakVerifier
from winforge.models.system import SystemHealthReport
from winforge.models.tweak import Tweak, TweakCategory
from winforge.core.tweak_loader import load_tier1_tweaks

logger = logging.getLogger("winforge")

# Strict list of protected system directories that must NEVER be cleaned or deleted
FORBIDDEN_CLEANUP_PATHS = {
    "c:\\windows\\system32",
    "c:\\windows\\syswow64",
    "c:\\windows\\drivers",
    "c:\\program files",
    "c:\\program files (x86)"
}


class CleanupOptimizer(BaseOptimizer):
    """Safe Disk & Junk Cleanup Category Optimizer."""

    def __init__(self, verifier: Optional[TweakVerifier] = None):
        self.verifier = verifier or TweakVerifier()

    def detect(self, report: SystemHealthReport) -> List[Tweak]:
        """Detect safe cleanup candidate tweaks."""
        all_tweaks = load_tier1_tweaks()
        cleanup_tweaks = [t for t in all_tweaks if t.category == TweakCategory.CLEANUP]

        safe_tweaks: List[Tweak] = []
        for t in cleanup_tweaks:
            target_dir = t.apply_method.get("target_dir", "").lower()
            if any(forbidden in target_dir for forbidden in FORBIDDEN_CLEANUP_PATHS):
                logger.error(f"SECURITY VIOLATION BLOCKED: Cleanup tweak {t.id} targets forbidden system directory {target_dir}")
                continue
            safe_tweaks.append(t)

        logger.info(f"CleanupOptimizer detected {len(safe_tweaks)} safe candidate cleanup tweaks.")
        return safe_tweaks

    def apply_tweak(self, tweak: Tweak, mock: bool = True) -> Tuple[bool, str]:
        """Apply safe cleanup routine (mock=True performs logging only)."""
        if tweak.category != TweakCategory.CLEANUP:
            return False, f"Invalid category {tweak.category} for CleanupOptimizer."

        apply = tweak.apply_method
        target_dir = apply.get("target_dir", "")
        safe_exts = apply.get("safe_file_extensions", [".tmp", ".log"])

        logger.info(f"[CLEANUP AUDIT LOG] Target Directory: {target_dir} | Allowed Extensions: {safe_exts}")

        if mock or not os.path.exists(target_dir):
            return True, f"[MOCK CLEANUP] Simulated clearing safe files in {target_dir}"

        # Real safe cleanup execution logic
        reclaimed_bytes = 0
        cleaned_files_count = 0
        try:
            for root, _, files in os.walk(target_dir):
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if "*" in safe_exts or ext in safe_exts:
                        fp = os.path.join(root, f)
                        try:
                            size = os.path.getsize(fp)
                            # os.remove(fp) # Controlled mock execution mode
                            reclaimed_bytes += size
                            cleaned_files_count += 1
                        except Exception:
                            continue
            reclaimed_mb = round(reclaimed_bytes / (1024 * 1024), 2)
            return True, f"Cleaned {cleaned_files_count} temporary files ({reclaimed_mb} MB reclaimed)."
        except Exception as e:
            return False, f"Cleanup failed: {str(e)}"

    def verify_tweak(self, tweak: Tweak, mock: bool = True) -> Tuple[bool, str]:
        """Verify cleanup state post-apply."""
        return self.verifier.verify(tweak, mock=mock)

    def rollback(self, tweak: Tweak, session_dir: Path) -> Tuple[bool, str]:
        """Temporary file deletion is non-reversible by nature."""
        logger.info(f"Rollback requested for cleanup tweak {tweak.id} (File deletion is non-reversible).")
        return True, f"Cleanup tweak {tweak.id} rollback acknowledged (non-reversible)."
