from winforge.core.engine import run_full_system_scan, run_session_pipeline
from winforge.core.session import SessionManager


def test_session_manager_lifecycle():
    mgr = SessionManager()
    assert mgr.session_id != ""
    assert mgr.session_dir.exists()

    report = run_full_system_scan()
    file_path = mgr.save_diagnostic_report("before.json", report)
    assert file_path.exists()


def test_full_session_pipeline():
    session_mgr, report, bench, sim_res = run_session_pipeline(dry_run=True, run_benchmarks=False)
    assert session_mgr.session_dir.exists()
    assert report.health_score > 0
    assert (session_mgr.session_dir / "report.html").exists()


def test_session_summary_and_rollback_location_compatibility(tmp_path):
    mgr = SessionManager()
    summary_path = mgr.save_session_summary({"test": True, "applied": 2})
    assert summary_path.exists()
    assert summary_path.name == "session_summary.json"

    from winforge.safety.rollback_engine import RollbackEngine
    from winforge.models.rollback import RollbackTransaction
    tx = RollbackTransaction(transaction_id=mgr.session_id, timestamp="2026-07-29T00:00:00Z", actions=[])
    mgr.save_rollback_ledger(tx)

    engine = RollbackEngine()
    found_dir, loc_label = engine.find_session_dir(mgr.session_id)
    assert found_dir is not None
    assert mgr.session_id in str(found_dir)

    # Test direct path resolution when session folder is moved to custom external location
    moved_dir = tmp_path / "EXTERNAL_MOVED_SESSION"
    moved_dir.mkdir(parents=True, exist_ok=True)
    (moved_dir / "rollback.json").write_text("{}", encoding="utf-8")

    found_path, direct_label = engine.find_session_dir(str(moved_dir))
    assert found_path == moved_dir
    assert "Direct Path" in direct_label
