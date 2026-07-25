import json
import logging
from pathlib import Path
from typing import Optional

from winforge.licensing.models import (
    ValidationState, LicenseType, LicenseCapabilities, ValidationResult
)
from winforge.licensing.verifier import LicenseVerifier
from winforge.licensing.fingerprint import FingerprintRecord
from winforge.utils.paths import get_app_dir

logger = logging.getLogger("winforge")


class LicensePolicyManager:
    """Manages business tier licensing policies and feature gating safely."""

    def __init__(self, verifier: Optional[LicenseVerifier] = None):
        self.verifier = verifier or LicenseVerifier()

    def get_active_license(
        self,
        license_file_path: Optional[Path] = None,
        mock_record: Optional[FingerprintRecord] = None
    ) -> ValidationResult:
        """Loads and verifies local license file, falling back safely to FREE_EDITION if unlicensed."""
        if not license_file_path:
            license_file_path = get_app_dir() / "licenses" / "license.json"

        if not license_file_path.exists():
            logger.info("No license.json file found. Operating in FREE_EDITION mode.")
            return ValidationResult(
                state=ValidationState.VALID,
                message="No license file present. Standard FREE_EDITION active.",
                capabilities=LicenseCapabilities(tier=LicenseType.FREE_EDITION)
            )

        try:
            with open(license_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            res = self.verifier.verify_license_payload(data, current_record=mock_record)
            logger.info(f"License evaluation completed: {res.state.value} (Tier: {res.capabilities.tier.value})")
            return res
        except Exception as e:
            logger.error(f"Failed parsing license file {license_file_path}: {e}")
            return ValidationResult(
                state=ValidationState.CORRUPTED_LICENSE,
                message=f"License file corrupted: {str(e)}",
                capabilities=LicenseCapabilities(tier=LicenseType.FREE_EDITION)
            )
