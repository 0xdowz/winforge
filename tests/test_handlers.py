from winforge.optimizations.registry_handler import RegistryHandler
from winforge.optimizations.service_handler import ServiceHandler
from winforge.core.tweak_loader import load_tier1_tweaks
from winforge.models.tweak import RiskCategory


def test_registry_handler_mock():
    reg = RegistryHandler()
    # Read test
    ok, val, msg = reg.read_registry_value("HKLM", "SOFTWARE\\Test", "TestVal")
    assert isinstance(ok, bool)

    # Write test (mock=True)
    w_ok, w_msg = reg.write_registry_value("HKLM", "SOFTWARE\\Test", "TestVal", "REG_DWORD", 1, mock=True)
    assert w_ok is True
    assert "[MOCK WRITE]" in w_msg


def test_service_handler_mock():
    svc = ServiceHandler()
    # Query status for RpcSs (available on all Windows Server and Desktop platforms)
    q_ok, q_info = svc.get_service_status("RpcSs")
    assert q_ok is True
    assert q_info.get("name", "").lower() == "rpcss"

    # Config start type (mock=True)
    s_ok, s_msg = svc.set_service_start_type("RpcSs", "demand", mock=True)
    assert s_ok is True
    assert "[MOCK SERVICE]" in s_msg


def test_tweak_risk_scoring_schemas():
    tweaks = load_tier1_tweaks()
    assert len(tweaks) >= 15
    for t in tweaks:
        assert 0 <= t.risk_score <= 100
        assert isinstance(t.risk_category, RiskCategory)
        if t.id == "TWEAK_GAME_004":
            assert t.risk_score == 85
            assert t.risk_category == RiskCategory.TECHNICIAN_ONLY
            assert t.technician_only is True
