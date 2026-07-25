"""
VENDOR TOOL ONLY - NOT INCLUDED IN CLIENT EXECUTABLE
Signs License Payloads using Private RSA-2048 Key & RSA-PSS.
"""

import json
import base64
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def sign_license_payload(
    private_key_pem: bytes,
    license_id: str,
    customer_id: str,
    license_type: str,
    target_fingerprint_hash: str,
    valid_days: int = 365,
    unlimited: bool = False
) -> Dict[str, Any]:
    """Signs a license payload using RSA-PSS and private key."""

    priv_key = serialization.load_pem_private_key(private_key_pem, password=None)
    created_at = datetime.now()
    expires_at = created_at + timedelta(days=valid_days)

    payload = {
        "schema_version": "2.0.0",
        "license_id": license_id,
        "license_type": license_type,
        "customer_id": customer_id,
        "created_at": created_at.isoformat() + "Z",
        "expires_at": expires_at.isoformat() + "Z",
        "fingerprint_version": 1,
        "machine_fingerprint": target_fingerprint_hash,
        "feature_flags": {
            "technician_mode_allowed": license_type in ("TECHNICIAN", "PROFESSIONAL"),
            "unlimited_machines": unlimited or license_type == "TECHNICIAN",
            "custom_branding_allowed": license_type == "TECHNICIAN",
            "offline_activation": True
        },
        "max_activations": 99999 if unlimited else 1,
        "activation_history": [
            {"timestamp": created_at.isoformat() + "Z", "machine_hash": target_fingerprint_hash}
        ],
        "revocation_status": False
    }

    # Canonicalize and sign
    canonical_json = json.dumps(payload, sort_keys=True)
    signature_bytes = priv_key.sign(
        canonical_json.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    payload["signature"] = base64.b64encode(signature_bytes).decode("utf-8")
    return payload
