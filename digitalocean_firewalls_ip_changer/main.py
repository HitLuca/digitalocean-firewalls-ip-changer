"""
main entrypoint for the cli interface
"""
import logging
import sys
from pathlib import Path

import click

sys.path.append(str(Path(__file__).resolve().parents[1]))

from digitalocean_firewalls_ip_changer.custom_logging import LoggingLevels, setup_logger
from digitalocean_firewalls_ip_changer.constants import LOG_FILEPATH
from digitalocean_firewalls_ip_changer.firewall_updater import update_firewalls


logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--logging-level",
    type=click.Choice([logging_level.name for logging_level in LoggingLevels]),
    default=LoggingLevels.INFO.name,
    help="Logging level to use",
    show_default=True,
)
def main(logging_level: str) -> None:
    """
    main cli entrypoint

    Args:
        logging_level (str): logging level to use
    """
    setup_logger(LOG_FILEPATH, LoggingLevels[logging_level])
    update_firewalls()


if __name__ == "__main__":
    main()  # pylint:disable=no-value-for-parameter
