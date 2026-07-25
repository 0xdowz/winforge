from enum import Enum
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class TweakState(str, Enum):
    DISCOVERED = "DISCOVERED"
    ANALYZED = "ANALYZED"
    RECOMMENDED = "RECOMMENDED"
    APPROVED = "APPROVED"
    BACKUP_COMPLETED = "BACKUP_COMPLETED"
    EXECUTING = "EXECUTING"
    VERIFIED = "VERIFIED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ROLLBACK_PENDING = "ROLLBACK_PENDING"
    ROLLED_BACK = "ROLLED_BACK"


class TweakExecutionTracker(BaseModel):
    tweak_id: str
    name: str
    current_state: TweakState = TweakState.DISCOVERED
    state_history: List[Dict[str, Any]] = Field(default_factory=list)
    captured_before_state: Optional[Dict[str, Any]] = None
    captured_after_state: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

    def transition_to(self, new_state: TweakState, reason: str = ""):
        """Transitions state machine to new state and records timestamp."""
        record = {
            "from_state": self.current_state.value,
            "to_state": new_state.value,
            "timestamp": datetime.now().isoformat(),
            "reason": reason
        }
        self.current_state = new_state
        self.state_history.append(record)
