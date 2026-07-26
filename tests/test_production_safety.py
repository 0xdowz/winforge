from pathlib import Path
from unittest.mock import patch

from winforge.models.tweak import Tweak, TweakCategory, RiskCategory
from winforge.optimizations.dispatcher import CategoryDispatcher
from winforge.optimizations.executor import OptimizationExecutor
from winforge.optimizations.registry_handler import RegistryHandler
from winforge.core.engine import run_full_system_scan
from winforge.core.session import SessionManager


def test_category_dispatcher_routing():
    dispatcher = CategoryDispatcher()
    report = run_full_system_scan()
    tweaks = dispatcher.detect_all_candidate_tweaks(report)
    assert len(tweaks) >= 15

    for t in tweaks:
        opt = dispatcher.get_optimizer(t.category)
        assert opt is not None

        ok, msg = dispatcher.apply_tweak(t, mock=True)
        assert ok is True

        v_ok, v_msg = dispatcher.verify_tweak(t, mock=True)
        assert v_ok is True


def test_client_mode_risk_tier_restriction():
    executor = OptimizationExecutor()
    report = run_full_system_scan()
    session_mgr = SessionManager()

    # Technician-only tweak (Risk Score 85)
    tech_tweak = Tweak(
        id="TWEAK_GAME_004",
        name="Network Throttling Index",
        description="Technician tweak",
        category=TweakCategory.GAMING,
        risk_score=85,
        risk_category=RiskCategory.TECHNICIAN_ONLY,
        technician_only=True,
        detection_logic={}, apply_method={}, rollback_method={}
    )

    # Attempt execution in Client Mode (is_tech_mode=False)
    tracker, res = executor.process_tweak_pipeline(
        tweak=tech_tweak,
        report=report,
        session_mgr=session_mgr,
        is_tech_mode=False,
        user_approved=True,
        mock_execution=True
    )

    # Must be SKIPPED due to RISK TIER RESTRICTED
    assert res.status.value == "SKIPPED"
    assert "RISK TIER RESTRICTED" in res.message


def test_technician_mode_allowed_risk_tweak(client_system_report, mock_admin_privileges):
    executor = OptimizationExecutor()
    session_mgr = SessionManager()

    tech_tweak = Tweak(
        id="TWEAK_GAME_004",
        name="Network Throttling Index",
        description="Technician tweak",
        category=TweakCategory.GAMING,
        risk_score=85,
        risk_category=RiskCategory.TECHNICIAN_ONLY,
        technician_only=True,
        detection_logic={}, apply_method={"type": "registry", "key": "HKLM\\Software\\Test"}, rollback_method={}
    )

    # Attempt execution in Technician Mode (is_tech_mode=True) on Client OS
    tracker, res = executor.process_tweak_pipeline(
        tweak=tech_tweak,
        report=client_system_report,
        session_mgr=session_mgr,
        is_tech_mode=True,
        user_approved=True,
        mock_execution=True
    )

    # Must succeed in Technician mode on Client OS
    assert tracker.current_state.value == "COMPLETED"


def test_server_mode_gaming_tweak_blocked(server_system_report, mock_admin_privileges):
    """Verifies that Gaming tweaks are strictly blocked on Windows Server OS to preserve server stability."""
    executor = OptimizationExecutor()
    session_mgr = SessionManager()

    tech_tweak = Tweak(
        id="TWEAK_GAME_004",
        name="Network Throttling Index",
        description="Technician tweak",
        category=TweakCategory.GAMING,
        risk_score=85,
        risk_category=RiskCategory.TECHNICIAN_ONLY,
        technician_only=True,
        detection_logic={}, apply_method={"type": "registry", "key": "HKLM\\Software\\Test"}, rollback_method={}
    )

    tracker, res = executor.process_tweak_pipeline(
        tweak=tech_tweak,
        report=server_system_report,
        session_mgr=session_mgr,
        is_tech_mode=True,
        user_approved=True,
        mock_execution=True
    )

    # Must fail policy check on Windows Server OS
    assert tracker.current_state == TweakState.FAILED
    assert res.status.value == "SKIPPED"
    assert "Policy Blocked" in res.message


def test_real_registry_isolated_test_key():
    """Isolated test verifying write, read, and rollback against HKCU\\Software\\WinForgeTest."""
    handler = RegistryHandler()
    hive = "HKCU"
    key_path = r"Software\WinForgeTest"
    val_name = "TestState"

    # Step 1: Write initial baseline value
    w_ok, w_msg = handler.write_registry_value(hive, key_path, val_name, "REG_SZ", "Original", mock=False)
    assert w_ok is True

    # Step 2: Read baseline value
    r_ok, val, r_msg = handler.read_registry_value(hive, key_path, val_name)
    assert r_ok is True
    assert val == "Original"

    # Step 3: Write optimized test value
    o_ok, o_msg = handler.write_registry_value(hive, key_path, val_name, "REG_SZ", "Optimized", mock=False)
    assert o_ok is True

    # Step 4: Verify write
    r_ok2, val2, _ = handler.read_registry_value(hive, key_path, val_name)
    assert val2 == "Optimized"

    # Step 5: Rollback to original baseline
    rb_ok, rb_msg = handler.write_registry_value(hive, key_path, val_name, "REG_SZ", "Original", mock=False)
    assert rb_ok is True

    # Step 6: Verify rollback
    r_ok3, val3, _ = handler.read_registry_value(hive, key_path, val_name)
    assert val3 == "Original"
