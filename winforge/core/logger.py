import logging
import sys
from pathlib import Path
from winforge.utils.paths import get_logs_dir


def setup_logger(log_level: int = logging.INFO) -> logging.Logger:
    """Configures centralized winforge logger with console and rotating file handlers."""
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
