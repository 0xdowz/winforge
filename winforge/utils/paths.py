import os
import sys
from pathlib import Path


def get_app_dir() -> Path:
    """Returns local application directory for WinForge logs, sessions, and configuration."""
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path.home() / ".config"

    app_dir = base / "WinForge"
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


def get_logs_dir() -> Path:
    """Returns directory for application runtime log files."""
    d = get_app_dir() / "logs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_reports_dir() -> Path:
    """Returns directory for exported HTML and JSON reports."""
    d = get_app_dir() / "reports"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_bundle_dir() -> Path:
    """Returns path to application bundle root directory (supports PyInstaller frozen binary)."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent.parent


def get_config_dir() -> Path:
    """Returns configuration directory path."""
    return get_bundle_dir() / "config"
