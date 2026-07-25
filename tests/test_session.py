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
