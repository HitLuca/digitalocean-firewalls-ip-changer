"""
logging related module
"""
import logging
import sys
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class LoggingLevels(Enum):
    """
    allowed logging levels
    """

    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING


def setup_logger(log_filepath: Path, logging_level: LoggingLevels) -> None:
    """
    sets up the logging facility for when design_engine is run from cli

    Args:
        log_filepath (Path): filepath for the output log file
        logging_level (LoggingLevels): logging level to use (info, warning, etc))
    """

    def _exception_hook(*exc_info):
        """
        exception hook used to log any unhandled exception before throwing
        """
        logger.exception("Exception", exc_info=exc_info)

    if log_filepath:
        log_folder = log_filepath.parents[0]

        if not log_folder.exists():
            log_folder.mkdir(parents=True)

    sys.excepthook = _exception_hook
    formatter_format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
    formatter = logging.Formatter(
        fmt=formatter_format,
        datefmt="%H:%M:%S" if logging_level == LoggingLevels.DEBUG else None,
    )
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)

    if log_filepath:
        logging.basicConfig(
            level=logging_level.value, format=formatter_format, filename=log_filepath
        )

    logging.getLogger().addHandler(stderr_handler)
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger("digitalocean_firewalls_ip_changer").setLevel(logging_level.value)
