import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from winforge.models.rollback import RollbackTransaction, RollbackAction

logger = logging.getLogger("winforge")


class TransactionManager:
    """Manages transactional state records for applied optimizations."""

    def __init__(self, session_id: str, session_dir: Path):
        self.session_id = session_id
        self.session_dir = session_dir
        self.ledger_path = session_dir / "rollback.json"
        self.transaction = RollbackTransaction(
            transaction_id=session_id,
            timestamp=datetime.now().isoformat(),
            actions=[]
        )

    def record_action(
        self,
        tweak_id: str,
        action_type: str,
        target: str,
        previous_value: str,
        new_value: str
    ):
        """Append an atomic action record to the transaction ledger."""
        action = RollbackAction(
            tweak_id=tweak_id,
            action_type=action_type,
            target=target,
            previous_value=previous_value,
            new_value=new_value,
            timestamp=datetime.now().isoformat()
        )
        self.transaction.actions.append(action)
        self.save()

    def save(self):
        """Write rollback transaction ledger to disk."""
        with open(self.ledger_path, "w", encoding="utf-8") as f:
            f.write(self.transaction.model_dump_json(indent=2))
        logger.debug(f"Rollback ledger updated at: {self.ledger_path}")
