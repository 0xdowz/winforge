import os
import sys
from pathlib import Path


def get_executable_dir() -> Path:
    """Returns absolute stable path to executable parent directory or project root."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent.parent


def get_app_dir() -> Path:
    """Returns local application directory for WinForge logs, sessions, and configuration."""
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path.home() / ".config"

    app_dir = (base / "WinForge").resolve()
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


def get_desktop_dir() -> Path:
    """
    Safely resolves current user's Desktop directory using Windows Shell Known Folder APIs.
    Supports standard Desktop, OneDrive-redirected Desktop, and non-English Windows installations.
    """
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes
            buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
            # CSIDL_DESKTOPDIRECTORY = 0x0010, SHGFP_TYPE_CURRENT = 0
            if ctypes.windll.shell32.SHGetFolderPathW(None, 0x0010, None, 0, buf) == 0:
                p = Path(buf.value)
                if p.exists():
                    return p
        except Exception:
            pass

        onedrive_desktop = Path.home() / "OneDrive" / "Desktop"
        if onedrive_desktop.exists():
            return onedrive_desktop

    default_desktop = Path.home() / "Desktop"
    default_desktop.mkdir(parents=True, exist_ok=True)
    return default_desktop


def get_output_mode() -> str:
    """Returns configured output mode: 'DESKTOP' (default) or 'LOCALAPPDATA'."""
    return os.environ.get("WINFORGE_OUTPUT_MODE", "DESKTOP").upper()


def get_user_reports_root() -> Path:
    """
    Returns the root directory for user-visible reports, sessions, diagnostics, and human logs.
    Defaults to 'Desktop\\WinForge Reports', but safely falls back to '%LOCALAPPDATA%\\WinForge\\UserReports'
    if Desktop creation fails due to PermissionError or filesystem restrictions.
    """
    mode = get_output_mode()
    if mode != "LOCALAPPDATA":
        try:
            root = get_desktop_dir() / "WinForge Reports"
            root.mkdir(parents=True, exist_ok=True)
            _ensure_readme_txt(root)
            return root
        except Exception:
            pass

    fallback_root = get_app_dir() / "UserReports"
    try:
        fallback_root.mkdir(parents=True, exist_ok=True)
        _ensure_readme_txt(fallback_root)
    except Exception:
        pass
    return fallback_root


def _ensure_readme_txt(root: Path):
    """Generates human-readable README.txt in WinForge Reports directory."""
    readme_path = root / "README.txt"
    if not readme_path.exists():
        content = """========================================================================
 WINFORGE USER REPORTS & DISASTER RECOVERY DIRECTORY
========================================================================

Welcome to your WinForge User Reports folder.

WinForge is an occasional Windows optimization and maintenance tool.
All user-facing diagnostic reports, optimization session ledgers, and
human-readable execution logs are saved here for easy access.

FOLDER STRUCTURE:
-----------------
  Sessions/     - Contains individual session ledgers, snapshots,
                  HTML reports, and rollback transaction files.
  Diagnostics/  - Contains HTML and JSON system diagnostic scan reports.
  Logs/         - Contains human-readable execution log files (winforge.log).

DISASTER RECOVERY & ONE-CLICK ROLLBACK:
--------------------------------------
To reverse all changes made in any optimization session, open Command
Prompt or PowerShell and run:

  WinForge.exe rollback <SESSION_ID>

Example:
  WinForge.exe rollback SESSION_20260729_024936_893FE1

OFFLINE & PRIVACY GUARANTEE:
---------------------------
WinForge operates 100% offline with zero telemetry and zero cloud connections.
Internal system state and crash traces remain protected in %LOCALAPPDATA%\\WinForge\\.

For full source code and documentation visit:
https://github.com/0xdowz/winforge
========================================================================
"""
        try:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            pass


def get_logs_dir() -> Path:
    """Returns directory for human-readable application execution logs (winforge.log)."""
    d = get_user_reports_root() / "Logs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_internal_logs_dir() -> Path:
    """Returns internal AppData directory for system crash traces & startup logs."""
    d = get_app_dir() / "logs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_reports_dir() -> Path:
    """Returns directory for user-facing diagnostic reports (system_scan.html, system_scan.json)."""
    d = get_user_reports_root() / "Diagnostics"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_sessions_dir() -> Path:
    """Returns directory for user-visible session ledgers (Sessions/)."""
    d = get_user_reports_root() / "Sessions"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_bundle_dir() -> Path:
    """Returns path to application bundle root directory (supports PyInstaller frozen binary)."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).resolve()
    return Path(__file__).resolve().parent.parent.parent


def get_config_dir() -> Path:
    """Returns configuration directory path."""
    return get_bundle_dir() / "config"
