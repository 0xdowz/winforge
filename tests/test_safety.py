from pathlib import Path
from winforge.safety.restore_point import create_system_restore_point
from winforge.safety.registry_backup import export_registry_key
from winforge.safety.snapshot import SystemSnapshotManager
from winforge.safety.transaction import TransactionManager
from winforge.safety.rollback_engine import RollbackEngine
from winforge.core.engine import run_full_system_scan


def test_restore_point_mock():
    ok, msg = create_system_restore_point("WINFORGE_TEST_RESTORE")
    assert isinstance(ok, bool)
    assert msg != ""


def test_registry_backup_mock(tmp_path: Path):
    target_file = tmp_path / "test_backup.reg"
    ok, msg = export_registry_key("HKLM\\SOFTWARE\\Microsoft", target_file)
    assert isinstance(ok, bool)


def test_snapshot_manager(tmp_path: Path):
    report = run_full_system_scan()
    mgr = SystemSnapshotManager()
    snap_path = mgr.create_snapshot(report, tmp_path)
    assert snap_path.exists()

    loaded = mgr.read_snapshot(snap_path)
    assert loaded is not None
    assert loaded["health_score"] == report.health_score


def test_transaction_and_rollback(tmp_path: Path):
    tx_mgr = TransactionManager("TEST_SESSION", tmp_path)
    tx_mgr.record_action("TWEAK_001", "REGISTRY", "HKLM\\Software\\Test", "0", "1")

    assert (tmp_path / "rollback.json").exists()

    rollback_eng = RollbackEngine()
    ok, logs = rollback_eng.rollback_session(tmp_path)
    assert ok is True
    assert len(logs) >= 1
