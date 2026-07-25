from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class ValidationState(str, Enum):
    VALID = "VALID"
    EXPIRED = "EXPIRED"
    INVALID_SIGNATURE = "INVALID_SIGNATURE"
    MACHINE_MISMATCH = "MACHINE_MISMATCH"
    CLOCK_SUSPICIOUS = "CLOCK_SUSPICIOUS"
    CORRUPTED_LICENSE = "CORRUPTED_LICENSE"
    UNSUPPORTED_VERSION = "UNSUPPORTED_VERSION"


class LicenseType(str, Enum):
    FREE_EDITION = "FREE_EDITION"
    PERSONAL = "PERSONAL"
    PROFESSIONAL = "PROFESSIONAL"
    TECHNICIAN = "TECHNICIAN"


class LicenseCapabilities(BaseModel):
    tier: LicenseType = Field(default=LicenseType.FREE_EDITION)
    technician_mode_allowed: bool = Field(default=False)
    max_risk_score_allowed: int = Field(default=20)
    unlimited_machines: bool = Field(default=False)
    custom_branding_allowed: bool = Field(default=False)
    offline_activation: bool = Field(default=True)


class LicensePayload(BaseModel):
    schema_version: str = Field(default="2.0.0")
    license_id: str = Field(..., description="Unique license ID e.g. LIC-2026-TECH-001")
    license_type: LicenseType = Field(default=LicenseType.FREE_EDITION)
    customer_id: str = Field(..., description="Customer identifier")
    created_at: str = Field(..., description="ISO timestamp when license was created")
    expires_at: str = Field(..., description="ISO timestamp when license expires")
    fingerprint_version: int = Field(default=1)
    machine_fingerprint: str = Field(..., description="Target machine fingerprint hash")
    feature_flags: Dict[str, bool] = Field(default_factory=dict)
    max_activations: int = Field(default=1)
    activation_history: List[Dict[str, Any]] = Field(default_factory=list)
    revocation_status: bool = Field(default=False)
    signature: str = Field(..., description="Base64 encoded RSA-PSS signature")


class ValidationResult(BaseModel):
    state: ValidationState
    message: str
    capabilities: LicenseCapabilities
    match_details: Optional[Dict[str, Any]] = None
