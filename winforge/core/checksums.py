import os
import json
import hashlib
import logging
from typing import Tuple, List, Dict
from winforge.utils.paths import get_config_dir

logger = logging.getLogger("winforge")


def verify_tweak_checksums() -> Tuple[bool, List[str]]:
    """
    Verifies SHA-256 integrity hashes for tweak database files against config/checksums.json.
    Returns (valid, warnings).
    """
    config_dir = get_config_dir()
    checksums_file = config_dir / "checksums.json"

    if not checksums_file.exists():
        msg = "Warning: config/checksums.json missing. Integrity verification skipped."
        logger.warning(msg)
        return True, [msg]

    try:
        with open(checksums_file, "r", encoding="utf-8") as f:
            expected = json.load(f)
    except Exception as e:
        msg = f"Warning: Failed loading config/checksums.json: {e}"
        logger.warning(msg)
        return True, [msg]

    warnings: List[str] = []
    all_valid = True

    for rel_path, expected_hash in expected.items():
        # Normalize path separators
        normalized_rel = rel_path.replace("\\", "/").replace("/", os.sep)
        target_file = config_dir / normalized_rel

        if not target_file.exists():
            warn_msg = f"INTEGRITY WARNING: Configuration file missing: {rel_path}"
            warnings.append(warn_msg)
            logger.warning(warn_msg)
            all_valid = False
            continue

        try:
            with open(target_file, "rb") as f:
                actual_hash = hashlib.sha256(f.read()).hexdigest()

            if actual_hash.lower() != expected_hash.lower():
                warn_msg = f"INTEGRITY WARNING: File modified or unverified: {rel_path}"
                warnings.append(warn_msg)
                logger.warning(warn_msg)
                all_valid = False
        except Exception as e:
            warn_msg = f"INTEGRITY WARNING: Error reading {rel_path}: {e}"
            warnings.append(warn_msg)
            logger.warning(warn_msg)
            all_valid = False

    return all_valid, warnings
