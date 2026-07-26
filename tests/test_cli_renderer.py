from rich.console import Console
from winforge.cli.theme import CONSOLE_WIDTH, render_section_header, format_short_path, RendererManager
from winforge.cli.banner import render_welcome_banner, render_banner
from winforge.cli.wizard import OptimizationWizard
from winforge.cli.renderer import render_optimization_plan, render_safety_lock_status, render_actionable_error, render_doctor_report
from winforge.cli.components import render_execution_report
from winforge.cli.themes import ThemeManager
from winforge.cli.formatting import format_status_badge, format_risk_badge
from winforge.cli.progress import StepTracker
from winforge.models.tweak import Tweak, TweakCategory, RiskLevel, RiskCategory
from winforge.safety.transaction import SafetyTransactionManager


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
    render_welcome_banner(tech_mode=False, dry_run=True)
    render_banner(tech_mode=True, dry_run=False)
    render_optimization_plan([tweak], is_tech_mode=False)
    render_safety_lock_status(restore_point_ready=True, registry_backup_ready=True, snapshot_ready=True)
    render_actionable_error(
        title="Optimization Blocked",
        reason="Windows Server OS detected.",
        suggested_action="Run on Windows 10/11."
    )
    render_doctor_report(is_admin=True, os_product="Windows 11 Pro", cpu_name="Test CPU", ram_gb=16.0, safety_ok=True)
    render_execution_report(completed_count=2, total_count=2, successful_count=2, skipped_count=0, skipped_reasons=[], delta_score=12.0)


def test_wizard_and_education_cards():
    tweak = Tweak(
        id="TWEAK_SAFE_001",
        name="GPU Scheduling Priority",
        description="Improves GPU scheduling behavior.",
        category=TweakCategory.GAMING,
        risk_level=RiskLevel.LOW,
        risk_score=10,
        risk_category=RiskCategory.SAFE,
        performance_gain_estimate="May improve frame consistency",
        user_visible_change="None",
        technician_only=False,
        detection_logic={}, apply_method={}, rollback_method={"type": "registry_delete"}
    )
    wiz = OptimizationWizard()
    wiz.render_tweak_education_card(tweak)


def test_cli_width_safety_limits(tmp_path):
    """Test console width limits across 80, 90, and 120 column terminals."""
    for w in [80, 90, 120]:
        rm = RendererManager(override_width=w)
        assert rm.width <= 90


def test_safety_transaction_manager_lifecycle(tmp_path):
    """Test centralized SafetyTransactionManager 7-step pre-flight safety execution."""
    stm = SafetyTransactionManager(session_id="TEST_SESSION_001", session_dir=tmp_path, mock_mode=True)
    pre_res = stm.execute_preflight_safety()
    
    assert pre_res["restore_point"] is True
    assert pre_res["registry_backup"] is True
    assert pre_res["snapshot"] is True
    
    stm.record_action(
        tweak_id="TWEAK_SAFE_001",
        action_type="registry_set",
        target="HKCU:\\Software\\Test",
        previous_value="0",
        new_value="1"
    )
    assert stm.ledger_path.exists()
