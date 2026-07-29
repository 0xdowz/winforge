import sys
import logging
from pathlib import Path
from unittest.mock import patch, MagicMock
from winforge.utils.paths import get_user_reports_root
from winforge.core.logger import setup_logger, log_startup_info, log_startup_exception


def test_user_reports_root_desktop_permission_error_fallback(monkeypatch, tmp_path):
    """Test get_user_reports_root falls back to AppData when Desktop throws PermissionError."""
    def mock_get_desktop_dir():
        raise PermissionError("Desktop folder access denied by policy")

    monkeypatch.setattr("winforge.utils.paths.get_desktop_dir", mock_get_desktop_dir)
    monkeypatch.setattr("winforge.utils.paths.get_app_dir", lambda: tmp_path / "AppDataWinForge")

    root = get_user_reports_root()
    assert root.exists()
    assert "UserReports" in str(root)
    assert (root / "README.txt").exists()


def _clear_logger():
    logger = logging.getLogger("winforge")
    for h in list(logger.handlers):
        logger.removeHandler(h)
        try:
            h.close()
        except Exception:
            pass


def test_logger_priority_1_desktop_success(tmp_path, monkeypatch):
    """Test logger uses Priority 1 Desktop log file when writable."""
    desktop_log_dir = tmp_path / "DesktopLogs"
    monkeypatch.setattr("winforge.core.logger.get_logs_dir", lambda: desktop_log_dir)

    _clear_logger()

    res_logger = setup_logger()
    assert len(res_logger.handlers) == 1
    assert isinstance(res_logger.handlers[0], logging.FileHandler)
    assert str(desktop_log_dir) in res_logger.handlers[0].baseFilename
    _clear_logger()


def test_logger_priority_2_appdata_fallback(tmp_path, monkeypatch):
    """Test logger falls back to Priority 2 AppData log when Desktop fails."""
    def mock_bad_logs_dir():
        raise PermissionError("Cannot access Desktop logs")

    appdata_log_dir = tmp_path / "AppDataLogs"
    monkeypatch.setattr("winforge.core.logger.get_logs_dir", mock_bad_logs_dir)
    monkeypatch.setattr("winforge.core.logger.get_internal_logs_dir", lambda: appdata_log_dir)

    _clear_logger()

    res_logger = setup_logger()
    assert len(res_logger.handlers) == 1
    assert isinstance(res_logger.handlers[0], logging.FileHandler)
    assert str(appdata_log_dir) in res_logger.handlers[0].baseFilename
    _clear_logger()


def test_logger_priority_3_console_fallback(monkeypatch):
    """Test logger falls back to Priority 3 StreamHandler when both Desktop and AppData fail."""
    def mock_bad_dir():
        raise PermissionError("Access denied")

    monkeypatch.setattr("winforge.core.logger.get_logs_dir", mock_bad_dir)
    monkeypatch.setattr("winforge.core.logger.get_internal_logs_dir", mock_bad_dir)

    _clear_logger()

    res_logger = setup_logger()
    assert len(res_logger.handlers) == 1
    assert isinstance(res_logger.handlers[0], logging.StreamHandler)
    _clear_logger()


def test_startup_logging_functions_never_crash(monkeypatch):
    """Test startup logging functions handle filesystem exceptions silently."""
    def mock_bad_dir():
        raise PermissionError("Access denied")

    monkeypatch.setattr("winforge.core.logger.get_internal_logs_dir", mock_bad_dir)

    # Should execute cleanly without raising exception
    log_startup_info(["--info"])
    log_startup_exception(RuntimeError("Test error"), "Unit test crash simulation")
