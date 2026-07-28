from unittest.mock import patch
from winforge.core.safety_approval import SafetyApprovalEngine, SafetyApprovalResult


def test_safety_approval_engine_structure():
    engine = SafetyApprovalEngine()
    res = engine.evaluate_realtime_safety()
    assert isinstance(res, SafetyApprovalResult)
    assert isinstance(res.approved, bool)
    assert isinstance(res.reason, str)


def test_safety_approval_mock_checks():
    with patch("winforge.core.safety_approval.is_admin", return_value=True):
        engine = SafetyApprovalEngine()
        res = engine.evaluate_realtime_safety(mock=True)
        assert res.approved is True


def test_safety_approval_simulated_mode():
    engine = SafetyApprovalEngine()
    res = engine.evaluate_realtime_safety(mock=True)
    assert res.approved is True
    assert "SIMULATED" in res.reason
