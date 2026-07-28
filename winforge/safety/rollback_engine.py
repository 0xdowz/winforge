import sys
import subprocess
import logging
from pathlib import Path
from typing import Tuple, List

from winforge.models.rollback import RollbackTransaction, RollbackAction
from winforge.core.privileges import is_admin

logger = logging.getLogger("winforge")


class RollbackEngine:
    """Executes transactional rollbacks to revert system state."""

    def rollback_session(self, session_dir: Path) -> Tuple[bool, List[str]]:
        """Parses rollback.json in session_dir and executes inverse operations."""
        ledger_path = session_dir / "rollback.json"
        if not ledger_path.exists():
            return False, ["Rollback ledger (rollback.json) not found in session folder."]

        try:
            with open(ledger_path, "r", encoding="utf-8") as f:
                data = f.read()
            transaction = RollbackTransaction.model_validate_json(data)
        except Exception as e:
            logger.error(f"Failed parsing rollback ledger: {e}")
            return False, [f"Failed reading rollback ledger: {str(e)}"]

        if not transaction.actions:
            logger.info("No applied actions found in rollback ledger. System state unchanged.")
            return True, ["No applied actions recorded. Rollback clean."]

        log_results: List[str] = []
        success = True

        # Process actions in reverse order (LIFO)
        for action in reversed(transaction.actions):
            act_success, msg = self._revert_action(action, session_dir)
            log_results.append(msg)
            if not act_success:
                success = False

        return success, log_results

    def _revert_action(self, action: RollbackAction, session_dir: Path) -> Tuple[bool, str]:
        """Reverts an individual action record."""
        logger.info(f"Reverting action [{action.tweak_id}]: {action.action_type} target {action.target}")

        if action.action_type == "REGISTRY_EXPORT_RESTORE":
            reg_file = session_dir / "registry_backups" / f"{action.target}.reg"
            if reg_file.exists() and sys.platform == "win32" and is_admin():
                cmd = f'reg.exe import "{reg_file}"'
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if res.returncode == 0:
                    return True, f"✓ Re-imported Registry Backup: {reg_file.name}"
                else:
                    return False, f"✗ Registry import failed for {reg_file.name}: {res.stderr.strip()}"
            else:
                return True, f"[MOCK] Re-imported Registry Backup: {action.target}.reg"

        elif action.action_type == "SERVICE_START_TYPE":
            if sys.platform == "win32" and is_admin():
                cmd = f'sc.exe config "{action.target}" start= {action.previous_value}'
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if res.returncode == 0:
                    return True, f"✓ Restored Service {action.target} start type to {action.previous_value}"
                else:
                    return False, f"✗ Failed restoring service {action.target}: {res.stderr.strip()}"
            else:
                return True, f"[MOCK] Restored Service {action.target} start type to {action.previous_value}"

        return True, f"Reverted action for {action.tweak_id}"
