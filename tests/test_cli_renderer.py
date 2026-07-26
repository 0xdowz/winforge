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
from winforge.models.system import SystemHealthReport, CPUInfo, RAMInfo, GPUInfo, PowerPlan, OSInfo, CategoryScores
from winforge.analyzers.hardware_profile import hardware_engine
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
    render_execution_report(
        session_id="TEST_SESSION_001",
        completed_count=2,
        total_count=2,
        successful_count=2,
        skipped_count=0,
        skipped_reasons=[],
        storage_recovered_gb=3.5,
        performance_gain_pct=18.0
    )


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


def test_hardware_intelligence_engine():
    report = SystemHealthReport(
        timestamp="2026-07-26T18:00:00",
        os=OSInfo(product_name="Windows 11 Pro"),
        cpu=CPUInfo(name="Intel Core i7-12700K", logical_cores=16, physical_cores=12, max_frequency_mhz=3600.0, current_usage_pct=15.0),
        ram=RAMInfo(total_gb=32.0, available_gb=16.0, used_gb=16.0, percent_used=50.0),
        gpu=[GPUInfo(name="NVIDIA GeForce RTX 4080", vram_mb=16384, driver_version="550.0")],
        drives=[],
        power=PowerPlan(active_name="High Performance", active_guid="...", is_on_battery=False),
        categories=CategoryScores(performance_score=100.0, security_score=100.0, maintenance_score=100.0, startup_score=100.0),
        health_score=90.0,
        startup_count=5,
        non_essential_services_count=10,
        warnings=[]
    )
    res = hardware_engine.analyze_hardware_profile(report)
    assert res["recommended_profile"] == "Gaming Performance Profile"
    assert res["has_discrete_gpu"] is True


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
