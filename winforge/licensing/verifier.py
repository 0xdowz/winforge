import os
import json
import base64
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Tuple

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

from winforge.licensing.models import (
    ValidationState, LicenseType, LicenseCapabilities, LicensePayload, ValidationResult
)
from winforge.licensing.fingerprint import FingerprintProvider, FingerprintMatcher, FingerprintRecord
from winforge.licensing.exceptions import InvalidSignatureError, LicenseExpiredError, MachineMismatchError

logger = logging.getLogger("winforge")

# Embedded RSA-2048 Public Verification Key for WinForge Client Runtime
DEFAULT_PUBLIC_KEY_PEM = b"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuX7GjO6mD/5aWvJ9a1+N
a8yVn0Q2Z3Z7xXwP6e5J0w2X9n8Z7y6W5v4U3t2S1r0Q9p8O7n6M5l4K3j2I1h0g
f9e8d7c6b5a4Y3X2W1V0U9T8S7R6Q5P4O3N2M1L0K9J8I7H6G5F4E3D2C1B0A9Z8
Y7X6W5V4U3T2S1R0Q9P8O7N6M5L4K3J2I1H0G5F4E3D2C1B0A9Z8Y7X6W5V4U3T2
S1R0Q9P8O7N6M5L4K3J2I1H0G5F4E3D2C1B0A9Z8Y7X6W5V4U3T2S1R0Q9P8O7N6
M5L4K3J2I1H0G5F4E3D2C1B0A9Z8Y7X6W5V4U3T2S1R0Q9P8O7N6M5L4K3J2I1H0
GwIDAQAB
-----END PUBLIC KEY-----"""


class LicenseVerifier:
    """RSA-PSS Signature Verifier & License Validator."""

    def __init__(self, public_key_pem: Optional[bytes] = None):
        self.public_key_pem = public_key_pem or DEFAULT_PUBLIC_KEY_PEM
        self.matcher = FingerprintMatcher()
        self.provider = FingerprintProvider()

    def verify_license_payload(
        self,
        payload_data: Dict[str, Any],
        current_record: Optional[FingerprintRecord] = None
    ) -> ValidationResult:
        """Validates payload schema, RSA-PSS signature, expiration date, and machine fingerprint."""
        # 1. Parse Schema
        try:
            payload = LicensePayload.model_validate(payload_data)
        except Exception as e:
            logger.error(f"License schema validation error: {e}")
            return ValidationResult(
                state=ValidationState.CORRUPTED_LICENSE,
                message=f"License JSON structure is corrupted: {str(e)}",
                capabilities=LicenseCapabilities(tier=LicenseType.FREE_EDITION)
            )

        # 2. RSA-PSS Signature Verification
        sig_bytes = base64.b64decode(payload.signature)
        canonical_json = self._canonicalize_payload(payload)

        try:
            pub_key = serialization.load_pem_public_key(self.public_key_pem)
            pub_key.verify(
                sig_bytes,
                canonical_json.encode("utf-8"),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        except Exception as sig_err:
            logger.warning(f"RSA-PSS Digital Signature Verification Failed: {sig_err}")
            return ValidationResult(
                state=ValidationState.INVALID_SIGNATURE,
                message="Digital signature verification failed. License file has been tampered with or corrupted.",
                capabilities=LicenseCapabilities(tier=LicenseType.FREE_EDITION)
            )

        # 3. Check Expiration Date
        try:
            exp_date = datetime.fromisoformat(payload.expires_at.replace("Z", "+00:00"))
            if datetime.now(exp_date.tzinfo) > exp_date:
                return ValidationResult(
                    state=ValidationState.EXPIRED,
                    message=f"License expired on {payload.expires_at}.",
                    capabilities=LicenseCapabilities(tier=LicenseType.FREE_EDITION)
                )
        except Exception as date_err:
            return ValidationResult(
                state=ValidationState.CORRUPTED_LICENSE,
                message=f"Invalid expiration date format: {date_err}",
                capabilities=LicenseCapabilities(tier=LicenseType.FREE_EDITION)
            )

        # 4. Machine Fingerprint Matching
        cur_fp = current_record or self.provider.collect_fingerprint()
        match_res = self.matcher.compare(cur_fp, payload.machine_fingerprint)

        if not match_res["activation_decision"] and not payload.feature_flags.get("unlimited_machines", False):
            return ValidationResult(
                state=ValidationState.MACHINE_MISMATCH,
                message=f"Machine fingerprint mismatch (Match score {match_res['match_score']}% < 75.0% required).",
                capabilities=LicenseCapabilities(tier=LicenseType.FREE_EDITION),
                match_details=match_res
            )

        # 5. Build Valid Capabilities
        capabilities = self._build_capabilities(payload)
        return ValidationResult(
            state=ValidationState.VALID,
            message="License signature and hardware fingerprint validated successfully.",
            capabilities=capabilities,
            match_details=match_res
        )

    def _canonicalize_payload(self, payload: LicensePayload) -> str:
        """Constructs canonical JSON string excluding signature for verification."""
        data = payload.model_dump()
        data.pop("signature", None)
        return json.dumps(data, sort_keys=True)

    def _build_capabilities(self, payload: LicensePayload) -> LicenseCapabilities:
        """Map license payload tier and feature flags to LicenseCapabilities."""
        tier = payload.license_type
        flags = payload.feature_flags

        if tier == LicenseType.TECHNICIAN:
            return LicenseCapabilities(
                tier=LicenseType.TECHNICIAN,
                technician_mode_allowed=True,
                max_risk_score_allowed=100,
                unlimited_machines=flags.get("unlimited_machines", True),
                custom_branding_allowed=flags.get("custom_branding_allowed", True)
            )
        elif tier == LicenseType.PROFESSIONAL:
            return LicenseCapabilities(
                tier=LicenseType.PROFESSIONAL,
                technician_mode_allowed=True,
                max_risk_score_allowed=80,
                unlimited_machines=False,
                custom_branding_allowed=False
            )
        elif tier == LicenseType.PERSONAL:
            return LicenseCapabilities(
                tier=LicenseType.PERSONAL,
                technician_mode_allowed=False,
                max_risk_score_allowed=50,
                unlimited_machines=False,
                custom_branding_allowed=False
            )

        return LicenseCapabilities(tier=LicenseType.FREE_EDITION)
