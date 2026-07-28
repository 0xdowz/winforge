"""
WinForge Centralized Logging Engine.
Provides application logger, startup logging (startup.log), and crash traceback recording.
"""

import sys
import os
import logging
import traceback
from datetime import datetime
from pathlib import Path
from winforge.utils.paths import get_logs_dir


def setup_logger(log_level: int = logging.INFO) -> logging.Logger:
    """Configures centralized winforge logger with file handler."""
    logger = logging.getLogger("winforge")
    logger.setLevel(log_level)

    if logger.handlers:
        return logger

    # File Handler
    log_file = get_logs_dir() / "winforge.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger


def get_startup_log_path() -> Path:
    """Returns path to startup.log."""
    return get_logs_dir() / "startup.log"


def log_startup_info(args_list: list):
    """Records application startup event, arguments, and environment to startup.log."""
    try:
        startup_file = get_startup_log_path()
        timestamp = datetime.now().isoformat()
        is_frozen = getattr(sys, "frozen", False)
        exe_path = sys.executable

        with open(startup_file, "a", encoding="utf-8") as f:
            f.write(f"\n==================================================\n")
            f.write(f"Startup Timestamp: {timestamp}\n")
            f.write(f"Executable:        {exe_path}\n")
            f.write(f"Is Frozen (Pyi):   {is_frozen}\n")
            f.write(f"Arguments:         {args_list}\n")
            f.write(f"Working Dir:       {os.getcwd()}\n")
            f.write(f"==================================================\n")
    except Exception:
        pass


def log_startup_exception(exc: Exception, reason: str = "Unhandled Runtime Exception"):
    """Records crash exception type, message, and traceback to startup.log."""
    try:
        startup_file = get_startup_log_path()
        timestamp = datetime.now().isoformat()
        tb_str = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))

        with open(startup_file, "a", encoding="utf-8") as f:
            f.write(f"\n[CRASH / EXCEPTION DETECTED - {timestamp}]\n")
            f.write(f"Reason:         {reason}\n")
            f.write(f"Exception Type: {type(exc).__name__}\n")
            f.write(f"Message:        {str(exc)}\n")
            f.write(f"Stack Trace:\n{tb_str}\n")
            f.write(f"==================================================\n")
    except Exception:
        pass
