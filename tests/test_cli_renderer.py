from rich.console import Console
from winforge.cli.theme import CONSOLE_WIDTH, render_section_header, format_short_path, RendererManager
from winforge.cli.banner import render_welcome_banner, render_banner
from winforge.cli.wizard import OptimizationWizard
from winforge.cli.renderer import render_optimization_plan, render_safety_lock_status, render_actionable_error, render_doctor_report, render_execution_report
from winforge.cli.themes import ThemeManager
from winforge.cli.formatting import format_status_badge, format_risk_badge
from winforge.cli.progress import StepTracker
from winforge.models.tweak import Tweak, TweakCategory, RiskLevel, RiskCategory
from winforge.models.system import SystemHealthReport, CPUInfo, RAMInfo, GPUInfo, PowerPlan, OSInfo, CategoryScores
from winforge.analyzers.hardware_profile import hardware_engine
from winforge.security.health import security_engine
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


def test_hardware_intelligence_engine_v2():
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
    
    # Assert complete schema contract existence
    required_keys = ["recommended_profile", "confidence_percent", "reasons", "rationale", "has_discrete_gpu", "is_on_battery"]
    for key in required_keys:
        assert key in res, f"Missing required hardware profile schema key: '{key}'"

    assert isinstance(res["recommended_profile"], str)
    assert isinstance(res["confidence_percent"], int)
    assert isinstance(res["reasons"], list)
    assert isinstance(res["rationale"], str)

    assert res["recommended_profile"] == "Gaming Performance Profile"
    assert res["confidence_percent"] == 92
    assert len(res["reasons"]) > 0
    assert "Dedicated GPU detected" in res["reasons"][0]
    assert len(res["rationale"]) > 0


def test_hardware_intelligence_engine_missing_data_fallback():
    """Verify hardware engine handles None reports and missing nested fields cleanly without exceptions."""
    res_none = hardware_engine.analyze_hardware_profile(None)
    assert res_none["recommended_profile"] == "Balanced Client Profile"
    assert res_none["confidence_percent"] == 80
    assert "rationale" in res_none
    assert len(res_none["reasons"]) > 0

    partial_report = SystemHealthReport(
        timestamp="2026-07-26T18:00:00",
        os=OSInfo(product_name="Windows 10"),
        cpu=CPUInfo(name="", logical_cores=0, physical_cores=0, max_frequency_mhz=0.0, current_usage_pct=0.0),
        ram=RAMInfo(total_gb=0.0, available_gb=0.0, used_gb=0.0, percent_used=0.0),
        gpu=[], drives=[],
        power=PowerPlan(active_name="Balanced", active_guid="...", is_on_battery=False),
        categories=CategoryScores(performance_score=80.0, security_score=80.0, maintenance_score=80.0, startup_score=80.0),
        health_score=80.0, startup_count=0, non_essential_services_count=0, warnings=[]
    )
    res_partial = hardware_engine.analyze_hardware_profile(partial_report)
    assert "recommended_profile" in res_partial
    assert "rationale" in res_partial
    assert res_partial["confidence_percent"] == 85


def test_security_health_engine():
    res = security_engine.audit_security_health()
    assert "security_score" in res
    assert res["security_score"] >= 0.0
    assert len(res["checks"]) >= 4


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
