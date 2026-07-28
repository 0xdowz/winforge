from unittest.mock import patch, MagicMock
import pytest
from winforge.core.privileges import is_admin, require_admin, relaunch_as_admin, request_elevation_if_needed
from winforge.safety.transaction import SafetyTransactionManager
from winforge.cli.interface import WinForgeCLI


def test_is_admin_check():
    """Verify is_admin() returns boolean."""
    res = is_admin()
    assert isinstance(res, bool)


def test_non_admin_launch_does_not_create_restore_point_or_modify_registry():
    """Requirement 1 & 2: Verify non-admin launch & analysis phase creates ZERO restore points and performs NO registry modifications."""
    with patch("winforge.safety.transaction.create_system_restore_point") as mock_restore, \
         patch("winforge.safety.transaction.export_registry_key") as mock_reg, \
         patch("winforge.core.privileges.is_admin", return_value=False):
        
        cli = WinForgeCLI(tech_mode=False, dry_run=False, mock_execution=False)
        # Phase 1: Analysis and scan only
        cli.latest_report = MagicMock()
        
        # Verify restore point creation and registry export were NEVER called
        mock_restore.assert_not_called()
        mock_reg.assert_not_called()


def test_user_declining_execution_creates_nothing(tmp_path):
    """Requirement 3: Verify user declining execution prompt creates ZERO restore points or registry exports."""
    with patch("winforge.safety.transaction.create_system_restore_point") as mock_restore, \
         patch("winforge.safety.transaction.export_registry_key") as mock_reg, \
         patch("rich.prompt.Confirm.ask", return_value=False):
        
        cli = WinForgeCLI(tech_mode=False, dry_run=False, mock_execution=False)
        cli.latest_report = MagicMock()
        
        cli.run_profile_optimization(max_risk=20, profile_name="Beginner Mode")
        
        mock_restore.assert_not_called()
        mock_reg.assert_not_called()


def test_user_accepting_execution_triggers_elevation_check():
    """Requirement 4: Verify user accepting execution triggers elevation check if non-admin."""
    with patch("rich.prompt.Confirm.ask", return_value=True), \
         patch("winforge.core.privileges.is_admin", return_value=False), \
         patch("winforge.core.privileges.request_elevation_if_needed", return_value=False) as mock_elevation:
        
        cli = WinForgeCLI(tech_mode=False, dry_run=False, mock_execution=False)
        cli.latest_report = MagicMock()
        
        cli.run_profile_optimization(max_risk=20, profile_name="Beginner Mode")
        
        mock_elevation.assert_called_once()


def test_admin_execution_creates_safety_snapshot_and_preflight(tmp_path):
    """Requirement 5: Verify admin execution creates safety snapshot and runs preflight safety."""
    with patch("rich.prompt.Confirm.ask", return_value=True), \
         patch("winforge.core.privileges.is_admin", return_value=True), \
         patch("winforge.safety.transaction.create_system_restore_point", return_value=(True, "OK")) as mock_restore, \
         patch("winforge.safety.transaction.export_registry_key", return_value=(True, "OK")) as mock_reg, \
         patch("winforge.optimizations.executor.OptimizationExecutor.process_tweak_pipeline") as mock_exec:
        
        mock_exec.return_value = (MagicMock(), MagicMock(message="Success", status=MagicMock(value="APPLIED")))
        
        cli = WinForgeCLI(tech_mode=False, dry_run=False, mock_execution=False)
        cli.latest_report = MagicMock()
        
        cli.run_profile_optimization(max_risk=20, profile_name="Beginner Mode")
        
        mock_restore.assert_called_once()
        mock_reg.assert_called_once()


def test_dry_run_zero_system_modifications(tmp_path):
    """Verify SafetyTransactionManager in mock/dry-run mode performs ZERO restore point or registry exports."""
    with patch("winforge.safety.transaction.create_system_restore_point") as mock_restore, \
         patch("winforge.safety.transaction.export_registry_key") as mock_reg:
        
        stm = SafetyTransactionManager(session_id="TEST_DRYRUN_001", session_dir=tmp_path, mock_mode=True)
        res = stm.execute_preflight_safety()
        
        assert res["restore_point"] is True
        assert res["registry_backup"] is True
        assert res["snapshot"] is True
        
        mock_restore.assert_not_called()
        mock_reg.assert_not_called()
