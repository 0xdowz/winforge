from winforge.cli.renderer import render_optimization_plan, render_safety_lock_status, render_actionable_error, render_doctor_report
from winforge.cli.themes import ThemeManager
from winforge.cli.formatting import format_status_badge, format_risk_badge
from winforge.cli.progress import StepTracker
from winforge.models.tweak import Tweak, TweakCategory, RiskLevel, RiskCategory


def test_cli_renderer_functions():
    tweak = Tweak(
        id="TWEAK_SAFE_001",
        name="Test Optimization Plan Tweak",
        description="Renderer unit test",
        category=TweakCategory.POWER,
        risk_level=RiskLevel.LOW,
        risk_score=10,
        risk_category=RiskCategory.SAFE,
        technician_only=False,
        detection_logic={}, apply_method={}, rollback_method={}
    )

    # Verify rendering functions execute cleanly without exceptions
    render_optimization_plan([tweak], is_tech_mode=False)
    render_safety_lock_status(restore_point_ready=True, registry_backup_ready=True, snapshot_ready=True)
    render_actionable_error(
        title="Optimization Blocked",
        reason="Windows Server OS detected.",
        suggested_action="Run on Windows 10/11."
    )
    render_doctor_report(is_admin=True, os_product="Windows 11 Pro", cpu_name="Test CPU", ram_gb=16.0, safety_ok=True)


def test_cli_design_system_components():
    tm = ThemeManager("dark")
    assert tm.get_style("primary") == "cyan"

    b1 = format_status_badge(90.0)
    assert b1 is not None

    r1 = format_risk_badge(10)
    assert "SAFE" in r1

    tracker = StepTracker("Test Pipeline", total_steps=2)
    tracker.log_step("Step 1", status="COMPLETED", success=True)
    tracker.finish("Pipeline completed successfully")
