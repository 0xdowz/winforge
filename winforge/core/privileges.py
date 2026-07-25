import sys
import ctypes
import os
import logging

logger = logging.getLogger("winforge")


def is_admin() -> bool:
    """Check if the current process is running with Administrative privileges."""
    if sys.platform != "win32":
        # Non-windows environment (e.g. testing)
        return os.environ.get("MOCK_ADMIN", "1") == "1"

    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        logger.warning(f"Failed to check admin status: {e}")
        return False


def require_admin() -> bool:
    """Verify admin privileges and log warning if not elevated."""
    admin_status = is_admin()
    if not admin_status:
        logger.warning("WinForge is running without Administrator privileges! Some modifications will fail.")
    return admin_status
