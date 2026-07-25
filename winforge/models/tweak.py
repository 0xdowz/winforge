from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


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
    detection_logic: Dict[str, Any] = Field(..., description="Logic to check current state")
    apply_method: Dict[str, Any] = Field(..., description="Instructions to execute tweak")
    rollback_method: Dict[str, Any] = Field(..., description="Instructions to revert tweak")
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
