"""
logging related module
"""
import logging
import logging.handlers
import sys
from enum import Enum
from pathlib import Path
from typing import Optional, Any

from digitalocean_firewalls_ip_changer.constants import PROJECT_NAME

logger = logging.getLogger(__name__)


class LoggingLevels(Enum):
    """
    allowed logging levels
    """

    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING


def setup_logger(log_filepath: Optional[Path], logging_level: LoggingLevels) -> None:
    """
    sets up the logging facility for when design_engine is run from cli

    Args:
        log_filepath (Optional[Path]): filepath for the output log file. If log_filepath is None then no logging is saved to file
        logging_level (LoggingLevels): logging level to use (info, warning, etc))
    """

    def _exception_hook(*exc_info: Any) -> None:
        """
        exception hook used to log any unhandled exception before throwing
        """
        logger.exception("Uncaught exception", exc_info=exc_info)  # type: ignore

    if log_filepath:
        log_folder = log_filepath.parents[0]

        if not log_folder.exists():
            log_folder.mkdir(parents=True)

    sys.excepthook = _exception_hook

    console_formatter = logging.Formatter(
        "%(levelname)s : %(name)s : %(message)s", datefmt=""
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging_level.value)

    if log_filepath:
        file_formatter = logging.Formatter(
            "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
        )
        file_handler = logging.handlers.RotatingFileHandler(
            log_filepath, maxBytes=5 * 1024 ^ 2, backupCount=1
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        logging.getLogger().addHandler(file_handler)

    logging.getLogger().addHandler(console_handler)

    logging.getLogger().setLevel(logging.WARNING)
    logging.getLogger(PROJECT_NAME).setLevel(logging.DEBUG)
