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
        friendly_name="Friendly Test Tweak",
        what_it_does="Cleans test files",
        why_it_exists="Prevents disk accumulation",
        exact_system_changes="Registry: HKLM\\Software\\Test = 1",
        detection_logic={},
        apply_method={},
        rollback_method={}
    )
    assert tweak.id == "TWEAK_001"
    assert tweak.category == TweakCategory.GAMING
    assert tweak.friendly_name == "Friendly Test Tweak"
    assert tweak.what_it_does == "Cleans test files"
    assert tweak.why_it_exists == "Prevents disk accumulation"
    assert tweak.exact_system_changes == "Registry: HKLM\\Software\\Test = 1"


def test_schema_validation_human_friendly_fallbacks():
    from winforge.models.tweak import validate_tweak_schema
    raw_data = {
        "id": "TWEAK_FB_001",
        "name": "Fallback Test Tweak",
        "description": "Fallback description",
        "rationale": "Fallback rationale",
        "category": "CLEANUP",
        "apply_method": {"type": "REGISTRY_DWORD", "key": "HKLM\\Software\\FB"}
    }
    ok, data, warnings = validate_tweak_schema(raw_data)
    assert ok is True
    assert data["friendly_name"] == "Fallback Test Tweak"
    assert data["what_it_does"] == "Fallback description"
    assert data["why_it_exists"] == "Fallback rationale"
    assert "REGISTRY_DWORD: HKLM\\Software\\FB" in data["exact_system_changes"]


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
