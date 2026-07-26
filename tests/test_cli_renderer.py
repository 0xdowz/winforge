from winforge.cli.renderer import render_optimization_plan, render_safety_lock_status, render_actionable_error
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
