from typing import Any, List, Optional
from pydantic import BaseModel, Field


class RollbackAction(BaseModel):
    tweak_id: str
    action_type: str  # e.g., REGISTRY, SERVICE, FILE, POWER_PLAN
    target: str       # e.g., registry key path, service name
    previous_value: Any
    new_value: Any
    timestamp: str


class RollbackTransaction(BaseModel):
    transaction_id: str
    timestamp: str
    restore_point_id: Optional[str] = None
    registry_backup_path: Optional[str] = None
    actions: List[RollbackAction] = Field(default_factory=list)
