from winforge.models.tweak import Tweak, RiskLevel, TweakCategory, TweakStatus
from winforge.models.system import CategoryScores, CPUInfo, RAMInfo, StorageDrive
from winforge.models.policy import DeviceProfile
from winforge.models.benchmark import BenchmarkSuiteResult


def test_tweak_model_validation():
    tweak = Tweak(
        id="TWEAK_001",
        name="Test Tweak",
        description="A test tweak",
        category=TweakCategory.GAMING,
        risk_level=RiskLevel.LOW,
        detection_logic={},
        apply_method={},
        rollback_method={}
    )
    assert tweak.id == "TWEAK_001"
    assert tweak.category == TweakCategory.GAMING


def test_category_scores_calculation():
    scores = CategoryScores(
        performance_score=80.0,
        security_score=90.0,
        maintenance_score=100.0,
        startup_score=70.0
    )
    assert scores.overall_health_score == 85.0


def test_device_profile_model():
    profile = DeviceProfile(
        is_laptop=True,
        is_server=False,
        is_domain_joined=False,
        is_on_battery=False,
        os_build=26200,
        total_ram_gb=16.0
    )
    assert profile.is_laptop is True
    assert profile.total_ram_gb == 16.0
