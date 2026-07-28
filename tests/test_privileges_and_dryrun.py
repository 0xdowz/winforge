from unittest.mock import patch, MagicMock
from winforge.core.privileges import is_admin, require_admin, relaunch_as_admin, request_elevation_if_needed
from winforge.safety.transaction import SafetyTransactionManager


def test_is_admin_check():
    """Verify is_admin() returns boolean."""
    res = is_admin()
    assert isinstance(res, bool)


def test_dry_run_zero_system_modifications(tmp_path):
    """Verify SafetyTransactionManager in mock/dry-run mode performs ZERO restore point or registry exports."""
    with patch("winforge.safety.transaction.create_system_restore_point") as mock_restore, \
         patch("winforge.safety.transaction.export_registry_key") as mock_reg:
        
        stm = SafetyTransactionManager(session_id="TEST_DRYRUN_001", session_dir=tmp_path, mock_mode=True)
        res = stm.execute_preflight_safety()
        
        assert res["restore_point"] is True
        assert res["registry_backup"] is True
        assert res["snapshot"] is True
        
        # Verify restore point creation and registry export were NEVER called
        mock_restore.assert_not_called()
        mock_reg.assert_not_called()


def test_production_mode_invokes_safety_locks(tmp_path):
    """Verify SafetyTransactionManager in production mode invokes restore point and registry export."""
    with patch("winforge.safety.transaction.create_system_restore_point", return_value=(True, "OK")) as mock_restore, \
         patch("winforge.safety.transaction.export_registry_key", return_value=(True, "OK")) as mock_reg:
        
        stm = SafetyTransactionManager(session_id="TEST_PROD_001", session_dir=tmp_path, mock_mode=False)
        res = stm.execute_preflight_safety()
        
        assert res["restore_point"] is True
        assert res["registry_backup"] is True
        
        mock_restore.assert_called_once()
        mock_reg.assert_called_once()


def test_request_elevation_if_needed_when_already_admin():
    """Verify request_elevation_if_needed returns True immediately if process is already admin."""
    with patch("winforge.core.privileges.is_admin", return_value=True):
        res = request_elevation_if_needed()
        assert res is True


def test_request_elevation_user_declined():
    """Verify request_elevation_if_needed returns False when user declines elevation prompt."""
    with patch("winforge.core.privileges.is_admin", return_value=False), \
         patch("rich.prompt.Prompt.ask", return_value="N"):
        res = request_elevation_if_needed()
        assert res is False
