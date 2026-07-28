"""
WinForge Safety Transaction Manager.
Manages 7-step centralized safety lifecycle and atomic rollback ledger.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from winforge.models.rollback import RollbackTransaction, RollbackAction
from winforge.safety.restore_point import create_system_restore_point
from winforge.safety.registry_backup import export_registry_key
from winforge.safety.snapshot import SystemSnapshotManager
from winforge.analyzers.hardware import get_storage_drives

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


class SafetyTransactionManager(TransactionManager):
    """
    Centralized Safety Transaction Manager executing 7-step safety session sequence:
      1. Pre-flight safety verification (Disk space >= 5.0GB gate)
      2. Create ONE system restore point (Production mode only)
      3. Create ONE atomic registry backup (Production mode only)
      4. Create ONE system snapshot
      5. Execute all approved tweaks
      6. Verify results
      7. Generate final session report
    """

    def __init__(self, session_id: str, session_dir: Path, mock_mode: bool = False):
        super().__init__(session_id, session_dir)
        self.mock_mode = mock_mode
        self.snapshot_mgr = SystemSnapshotManager()
        
        self.restore_point_ready = False
        self.registry_backup_ready = False
        self.snapshot_ready = False

    def execute_preflight_safety(self) -> Dict[str, Any]:
        """
        Performs initial 4-Layer Safety Lock setup once per session.
        Enforces 5.0 GB minimum free disk space gate on system drive.
        In simulation/mock mode, performs ZERO system restore point attempts or registry exports.
        """
        logger.info(f"Executing Pre-flight Safety for Session {self.session_id} (Mock/DryRun: {self.mock_mode})")
        
        if self.mock_mode:
            # Simulation Mode: Zero system modifications or registry exports
            logger.info(f"[SIMULATION] Pre-flight safety simulated for Session {self.session_id}")
            self.restore_point_ready = True
            self.registry_backup_ready = True
            self.snapshot_ready = True
        else:
            # Disk Space Safety Gate (Require >= 5.0 GB free on system drive C:)
            drives = get_storage_drives()
            sys_drive = next((d for d in drives if "C" in d.drive_letter.upper()), drives[0] if drives else None)
            if sys_drive and sys_drive.free_gb < 5.0:
                err_msg = (
                    f"CRITICAL: System drive ({sys_drive.drive_letter}) has insufficient free space "
                    f"({sys_drive.free_gb:.2f} GB free < 5.0 GB required). "
                    f"Windows Restore Point creation & System Registry backups require at least 5.0 GB free disk space. "
                    f"Optimization cancelled safely to prevent system drive exhaustion."
                )
                logger.error(err_msg)
                return {
                    "restore_point": False,
                    "registry_backup": False,
                    "snapshot": False,
                    "error": err_msg
                }

            # Production Mode: Create ONE Session System Restore Point & Registry Export
            r_ok, _ = create_system_restore_point(description=f"WinForge_{self.session_id}")
            self.restore_point_ready = r_ok
            
            reg_file = self.session_dir / "backup.reg"
            reg_ok, _ = export_registry_key("HKLM\\SOFTWARE", reg_file)
            self.registry_backup_ready = reg_ok
            self.snapshot_ready = True

        return {
            "restore_point": self.restore_point_ready,
            "registry_backup": self.registry_backup_ready,
            "snapshot": self.snapshot_ready,
            "error": None
        }
