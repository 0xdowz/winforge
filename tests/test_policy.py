from winforge.core.policy import PolicyEngine
from winforge.models.policy import DeviceProfile
from winforge.models.tweak import Tweak, RiskLevel, TweakCategory


def test_policy_engine_evaluation():
    engine = PolicyEngine()
    profile = DeviceProfile(
        is_laptop=True,
        is_server=False,
        is_domain_joined=False,
        is_on_battery=True,
        os_build=26200,
        total_ram_gb=16.0
    )

    tweak = Tweak(
        id="TWEAK_POWER_001",
        name="High Performance Power Plan",
        description="Sets power plan to High Performance",
        category=TweakCategory.POWER,
        risk_level=RiskLevel.LOW,
        supported_windows_versions=["10", "11"],
        detection_logic={}, apply_method={}, rollback_method={}
    )

    rule = engine.evaluate_tweak(tweak, profile)
    assert isinstance(rule.allowed, bool)
