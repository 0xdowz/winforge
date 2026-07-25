from winforge.core.engine import run_session_pipeline


def test_dry_run_pipeline():
    session_mgr, report, bench, sim_res = run_session_pipeline(dry_run=True, run_benchmarks=False)
    assert session_mgr.session_id != ""
    assert report.health_score > 0
    assert sim_res["simulated_health_score"] >= sim_res["baseline_health_score"]
    assert (session_mgr.session_dir / "findings.json").exists()
