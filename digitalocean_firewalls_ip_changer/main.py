import logging
import subprocess
import sys
from enum import Enum
from pathlib import Path

import requests
import yaml
from IPy import IP


sys.path.append(str(Path(__file__).resolve().parents[1]))

from digitalocean_firewalls_ip_changer.constants import (
    CONFIG_FILEPATH,
    IP_PROVIDER_URL,
    LOG_FILEPATH,
)

logger = logging.getLogger(__name__)


class FirewallRuleActions(Enum):
    ADD = "add-rules"
    REMOVE = "remove-rules"


def main() -> None:
    config = _load_config()

    new_ip = _get_new_ip()
    logger.info(f"new public ip: {new_ip}")

    logger.info(f"removing old firewall rules")
    _edit_firewall_rules(config, FirewallRuleActions.REMOVE)
    logger.info(f"old rules removed")

    logger.info(f"updating config")
    _update_config(config, new_ip)
    logger.info(f"config updated")

    logger.info(f"adding new firewall rules")
    _edit_firewall_rules(config, FirewallRuleActions.ADD)
    logger.info(f"new rules added")

    logger.info(f"saving config")
    _save_config(config)
    logger.info(f"config saved")


def _load_config() -> dict:
    with CONFIG_FILEPATH.open("r") as f:
        config = yaml.load(f, yaml.FullLoader)
    return config


def _edit_firewall_rules(config: dict, action: FirewallRuleActions) -> None:
    def _edit_firewall_rule(
        firewall_id: str,
        protocol: str,
        port: int,
        address: str,
        action: FirewallRuleActions,
    ) -> None:
        command = f'doctl compute firewall {FirewallRuleActions(action).value} {firewall_id} --inbound-rules "{_build_rule(protocol, port, address)}"'
        logger.info(f"sending command: {command}")
        result = subprocess.run(
            command, stdout=subprocess.PIPE, shell=True
        ).stdout.decode("utf-8")
        assert (
            result == ""
        ), f"firewall rule removal returned non-zero response: {result}"

    assert isinstance(action, FirewallRuleActions)

    for port in config["ports"]:
        _edit_firewall_rule(
            config["firewall_id"], config["protocol"], port, config["last_ip"], action
        )


def _build_rule(protocol: str, port: int, address: str) -> str:
    return f"protocol:{protocol},ports:{port},address:{address}"


def _get_new_ip(max_retries: int = 3) -> str:
    for _ in range(max_retries):
        new_ip = requests.get(IP_PROVIDER_URL).text
        try:
            IP(new_ip)
            return new_ip
        except ValueError:
            pass
    raise ValueError(f"cannot get new ip from {IP_PROVIDER_URL}")


def _update_config(config: dict, new_ip: str) -> None:
    config["past_ips"].append(config["last_ip"])
    config["last_ip"] = new_ip


def _save_config(config: dict) -> None:
    with CONFIG_FILEPATH.open("w") as f:
        yaml.dump(config, f)


def _setup_logger() -> None:
    formatter_format = "%(asctime)s : %(name)s : %(levelname)s : %(message)s"
    formatter = logging.Formatter(formatter_format)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    stdout_handler = logging.StreamHandler()
    logging.basicConfig(
        level=logging.INFO, format=formatter_format, filename=LOG_FILEPATH
    )
    logging.getLogger().addHandler(stdout_handler)


if __name__ == "__main__":
    _setup_logger()
    main()
