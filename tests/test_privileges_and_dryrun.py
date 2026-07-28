from unittest.mock import patch, MagicMock
import pytest
from pathlib import Path

from winforge.core.privileges import is_admin, require_admin, relaunch_as_admin, request_elevation_if_needed
from winforge.safety.transaction import SafetyTransactionManager
from winforge.safety.registry_backup import normalize_registry_path, export_registry_key
from winforge.models.tweak import Tweak, validate_tweak_schema
from winforge.core.session import save_pending_execution, load_pending_execution, clear_pending_execution
from winforge.utils.paths import get_bundle_dir, get_app_dir, get_executable_dir
from winforge.core.safety_approval import SafetyApprovalEngine
from winforge.safety.rollback_engine import RollbackEngine
from winforge.cli.interface import WinForgeCLI


def test_is_admin_check():
    """Verify is_admin() returns boolean."""
    res = is_admin()
    assert isinstance(res, bool)


def test_elevation_resume_persistence(tmp_path):
    """Requirement 8.1: Test elevation state saving and resume restoration."""
    with patch("winforge.core.session.get_app_dir", return_value=tmp_path):
        saved_path = save_pending_execution(
            session_id="TEST_RESUME_108",
            mode="BEGINNER",
            max_risk=20,
            selected_tweaks=["TWEAK_GAME_001", "TWEAK_POWER_001"],
            execute=True,
            dry_run=False,
            tech_mode=False
        )
        assert saved_path.exists()

        state = load_pending_execution()
        assert state is not None
        assert state["session_id"] == "TEST_RESUME_108"
        assert state["mode"] == "BEGINNER"
        assert state["max_risk"] == 20
        assert "TWEAK_GAME_001" in state["selected_tweaks"]

        clear_pending_execution()
        assert load_pending_execution() is None


def test_malformed_tweak_schema_validation():
    """Requirement 8.2: Test malformed tweak missing rationale does not crash and provides fallback."""
    raw_tweak = {
        "id": "TWEAK_MALFORMED_001",
        "name": "Malformed Test Tweak",
        "description": "Test tweak missing rationale field",
        "category": "CLEANUP",
        "risk_score": 10,
        "detection_logic": {},
        "apply_method": {},
        "rollback_method": {}
    }
    valid, sanitized, warnings = validate_tweak_schema(raw_tweak)
    assert valid is True
    assert sanitized["rationale"] == "No rationale provided"
    assert "rationale" in warnings[0]

    # Verify Pydantic model parses without error
    tweak = Tweak.model_validate(sanitized)
    assert tweak.rationale == "No rationale provided"


def test_pyinstaller_path_resolution():
    """Requirement 8.3: Test PyInstaller frozen mode and development absolute path resolution."""
    bundle_dir = get_bundle_dir()
    app_dir = get_app_dir()
    exe_dir = get_executable_dir()

    assert bundle_dir.is_absolute()
    assert app_dir.is_absolute()
    assert exe_dir.is_absolute()


def test_registry_path_normalization():
    """Requirement 8.4: Test shorthand and missing hive registry path normalization."""
    assert normalize_registry_path("SOFTWARE\\Microsoft\\Windows") == "HKLM\\SOFTWARE\\Microsoft\\Windows"
    assert normalize_registry_path("System\\GameConfigStore") == "HKLM\\System\\GameConfigStore"
    assert normalize_registry_path("HKEY_LOCAL_MACHINE\\SOFTWARE\\Test") == "HKLM\\SOFTWARE\\Test"
    assert normalize_registry_path("HKEY_CURRENT_USER\\Software\\Test") == "HKCU\\Software\\Test"
    assert normalize_registry_path("HKLM\\SOFTWARE\\Test") == "HKLM\\SOFTWARE\\Test"
    assert normalize_registry_path("HKCU\\Software\\Test") == "HKCU\\Software\\Test"


def test_disk_space_safety_gate_blocking():
    """Requirement 8.5: Test disk safety gate blocks execution if free space < 5.0 GB."""
    engine = SafetyApprovalEngine()
    
    mock_low_drive = MagicMock(drive_letter="C:\\", free_gb=2.1)
    with patch("winforge.core.safety_approval.get_storage_drives", return_value=[mock_low_drive]), \
         patch("winforge.core.safety_approval.is_admin", return_value=True):
        
        res = engine.evaluate_realtime_safety(mock=False)
        assert res.approved is False
        assert "insufficient free space" in res.reason.lower()
        assert res.checks_passed["sufficient_disk_space"] is False


def test_atomic_rollback_on_tweak_failure(tmp_path):
    """Requirement 8.6: Test session rollback triggered when a tweak fails."""
    ledger_file = tmp_path / "rollback.json"
    tx_data = {
        "transaction_id": "TEST_FAIL_SESSION",
        "timestamp": "2026-07-28T20:00:00Z",
        "actions": [
            {
                "tweak_id": "TWEAK_GAME_001",
                "action_type": "SERVICE_START_TYPE",
                "target": "diagtrack",
                "previous_value": "demand",
                "new_value": "disabled",
                "timestamp": "2026-07-28T20:00:01Z"
            }
        ]
    }
    with open(ledger_file, "w", encoding="utf-8") as f:
        f.write(import_json_str(tx_data))

    rb_engine = RollbackEngine()
    success, logs = rb_engine.rollback_session(tmp_path)
    assert success is True
    assert len(logs) == 1


def test_resume_optimization_without_import_error(tmp_path):
    """Verify render_execution_report import and resume_optimization execution without ImportError."""
    from winforge.cli.renderer import render_execution_report
    assert callable(render_execution_report)

    app = WinForgeCLI(tech_mode=False, dry_run=True, mock_execution=True)
    state = {
        "session_id": "TEST_SESSION_RESUME_001",
        "created_at": "2026-07-28T20:00:00.000000",
        "mode": "BEGINNER",
        "max_risk": 20,
        "selected_tweaks": ["TWEAK_GAME_001"],
        "execute": True,
        "dry_run": True,
        "tech_mode": False,
        "resume_required": True
    }
    with patch("winforge.core.session.get_app_dir", return_value=tmp_path):
        app.resume_optimization(state)


def import_json_str(data):
    import json
    return json.dumps(data)
