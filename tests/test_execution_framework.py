from pathlib import Path
from unittest.mock import patch

from winforge.models.tweak import Tweak, RiskLevel, TweakCategory, RiskCategory
from winforge.models.system import SystemHealthReport
from winforge.optimizations.state_machine import TweakState, TweakExecutionTracker
from winforge.optimizations.executor import OptimizationExecutor
from winforge.optimizations.verifier import TweakVerifier
from winforge.core.session import SessionManager
from winforge.core.engine import run_full_system_scan


def test_tweak_state_tracker():
    tracker = TweakExecutionTracker(tweak_id="TWEAK_001", name="Test Tweak")
    assert tracker.current_state == TweakState.DISCOVERED

    tracker.transition_to(TweakState.ANALYZED, reason="Policy check passed")
    assert tracker.current_state == TweakState.ANALYZED


def test_optimization_executor_mock(client_system_report, mock_admin_privileges):
    executor = OptimizationExecutor()
    session_mgr = SessionManager()

    dummy_tweak = Tweak(
        id="TWEAK_GAME_001",
        name="GPU Priority Optimization",
        description="Dummy test tweak",
        category=TweakCategory.GAMING,
        risk_level=RiskLevel.LOW,
        risk_score=10,
        risk_category=RiskCategory.SAFE,
        technician_only=False,
        detection_logic={},
        apply_method={"type": "registry", "hive": "HKLM", "key": "SOFTWARE\\Test", "value_name": "TestVal", "value_data": 1},
        rollback_method={"type": "registry", "hive": "HKLM", "key": "SOFTWARE\\Test", "value_name": "TestVal", "value_data": 0}
    )

    tracker, result = executor.process_tweak_pipeline(
        tweak=dummy_tweak,
        report=client_system_report,
        session_mgr=session_mgr,
        is_tech_mode=False,
        user_approved=True,
        mock_execution=True
    )

    assert tracker.current_state == TweakState.COMPLETED
    assert result.status.value == "SIMULATED"


def test_tweak_verifier_mock():
    verifier = TweakVerifier()
    dummy_tweak = Tweak(
        id="TWEAK_002",
        name="Verifier Test Tweak",
        description="Verifier test",
        category=TweakCategory.POWER,
        risk_level=RiskLevel.LOW,
        risk_score=10,
        risk_category=RiskCategory.SAFE,
        technician_only=False,
        detection_logic={}, apply_method={}, rollback_method={}
    )

    ok, msg = verifier.verify(dummy_tweak, mock=True)
    assert ok is True
    assert "[MOCK" in msg
