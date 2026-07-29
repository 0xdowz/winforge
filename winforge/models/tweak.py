import logging
from enum import Enum
from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Field

logger = logging.getLogger("winforge")


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RiskCategory(str, Enum):
    SAFE = "SAFE"                 # Score 0-20
    MODERATE = "MODERATE"         # Score 21-50
    ADVANCED = "ADVANCED"         # Score 51-80
    TECHNICIAN_ONLY = "TECHNICIAN_ONLY"  # Score 81-100


class TweakCategory(str, Enum):
    GAMING = "GAMING"
    CLEANUP = "CLEANUP"
    STARTUP = "STARTUP"
    SERVICES = "SERVICES"
    NETWORK = "NETWORK"
    POWER = "POWER"
    SECURITY_PRIVACY = "SECURITY_PRIVACY"


class TweakStatus(str, Enum):
    NOT_APPLIED = "NOT_APPLIED"
    APPLIED = "APPLIED"
    SKIPPED = "SKIPPED"
    FAILED = "FAILED"
    SIMULATED = "SIMULATED"


class Tweak(BaseModel):
    id: str = Field(..., description="Unique tweak identifier e.g. TWEAK_GAME_001")
    name: str = Field(..., description="Human readable tweak title")
    description: str = Field(..., description="Detailed explanation of what the tweak does")
    rationale: str = Field(default="No rationale provided", description="Technical rationale for applying this tweak")
    category: TweakCategory = Field(..., description="Optimization category")
    risk_level: RiskLevel = Field(default=RiskLevel.LOW, description="Safety risk classification")
    risk_score: int = Field(default=10, ge=0, le=100, description="Numeric risk score (0-100)")
    risk_category: RiskCategory = Field(default=RiskCategory.SAFE, description="Risk tier classification")
    schema_version: str = Field(default="2.0.0", description="Tweak database schema version")
    requires_admin: bool = Field(default=True, description="Whether elevation is required")
    requires_reboot: bool = Field(default=False, description="Whether reboot is required after apply")
    performance_gain_estimate: str = Field(default="Low", description="Estimated performance impact e.g. Low, Medium, High")
    user_visible_change: str = Field(default="None", description="Expected visible impact e.g. None, UI Refresh, Power Icon Change")
    technician_only: bool = Field(default=False, description="Whether tweak requires Technician approval")
    friendly_name: str = Field(default="", description="Non-intimidating title for non-technical users")
    what_it_does: str = Field(default="", description="Plain-English explanation of action taken")
    why_it_exists: str = Field(default="", description="Plain-English rationale for optimization")
    exact_system_changes: str = Field(default="", description="Formatted description of exact registry/service targets")
    detection_logic: Dict[str, Any] = Field(default_factory=dict, description="Logic to check current state")
    apply_method: Dict[str, Any] = Field(default_factory=dict, description="Instructions to execute tweak")
    rollback_method: Dict[str, Any] = Field(default_factory=dict, description="Instructions to revert tweak")
    verification_method: Dict[str, Any] = Field(default_factory=dict, description="Instructions to verify tweak state")


class TweakExecutionResult(BaseModel):
    tweak_id: str
    name: str
    category: TweakCategory
    status: TweakStatus
    timestamp: str
    message: str
    dry_run: bool = False
    details: Optional[Dict[str, Any]] = None


def validate_tweak_schema(tweak_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
    """
    Centralized Schema Validation System.
    Ensures every tweak dictionary contains required fields and injects safe fallbacks.
    Prevents KeyError crashes on malformed tweak metadata.
    """
    warnings: List[str] = []
    data = dict(tweak_data)

    if "id" not in data or not data["id"]:
        warnings.append("Missing required field: 'id'")
        data["id"] = "TWEAK_UNKNOWN"

    if "name" not in data or not data["name"]:
        warnings.append(f"Missing field 'name' on tweak {data['id']}; injected fallback.")
        data["name"] = data["id"]

    if "description" not in data or not data["description"]:
        warnings.append(f"Missing field 'description' on tweak {data['id']}; injected fallback.")
        data["description"] = "No description provided."

    if "rationale" not in data or not data["rationale"]:
        warnings.append(f"Missing field 'rationale' on tweak {data['id']}; injected fallback.")
        data["rationale"] = "No rationale provided"

    if "category" not in data or not data["category"]:
        warnings.append(f"Missing field 'category' on tweak {data['id']}; defaulting to CLEANUP.")
        data["category"] = "CLEANUP"

    if "risk" in data and "risk_score" not in data:
        data["risk_score"] = data["risk"]

    if "risk_score" not in data:
        data["risk_score"] = 10

    # User-friendly explanation fallbacks
    if "friendly_name" not in data or not data["friendly_name"]:
        data["friendly_name"] = data["name"]

    if "what_it_does" not in data or not data["what_it_does"]:
        data["what_it_does"] = data["description"]

    if "why_it_exists" not in data or not data["why_it_exists"]:
        data["why_it_exists"] = data["rationale"]

    if "exact_system_changes" not in data or not data["exact_system_changes"]:
        apply_method = data.get("apply_method", {})
        m_type = apply_method.get("type", "SYSTEM_MUTATION")
        m_key = apply_method.get("key") or apply_method.get("target") or apply_method.get("path") or data["id"]
        data["exact_system_changes"] = f"{m_type}: {m_key}"

    if warnings:
        logger.warning(f"[SCHEMA VALIDATION WARNING] {data['id']}: {'; '.join(warnings)}")

    return True, data, warnings
