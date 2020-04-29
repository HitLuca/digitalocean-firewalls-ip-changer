"""
firewall updating functionalities. Main entrypoint is update_firewalls
"""
import logging
from dataclasses import asdict
from enum import Enum
import subprocess

import requests
import yaml
from IPy import IP

from digitalocean_firewalls_ip_changer.config import Config
from digitalocean_firewalls_ip_changer.constants import (
    CONFIG_FILEPATH,
    IP_PROVIDER_URL,
)


logger = logging.getLogger(__name__)


class FirewallRuleActions(Enum):
    """
    firewall rule actions that can be taken
    """

    ADD = "add-rules"
    REMOVE = "remove-rules"


def update_firewalls() -> None:
    """
    updates the firewalls using a stored config, by first removing old rules and then
    updating them with new ones. Also updates the config and saves it
    """
    config = _load_config()

    new_ip = _get_public_ip()
    logger.info(f"new public ip: {new_ip}")

    if config.last_ip != "":
        logger.info("removing old firewall rules")
        _edit_firewall_rules(config, FirewallRuleActions.REMOVE)
        logger.info("old rules removed")

    logger.info("updating config")
    _update_config(config, new_ip)
    logger.info("config updated")

    logger.info("adding new firewall rules")
    _edit_firewall_rules(config, FirewallRuleActions.ADD)
    logger.info("new rules added")

    logger.info("saving config")
    _save_config(config)
    logger.info("config saved")


def _load_config() -> Config:
    """
    loads the firewalls config

    Raises:
        SystemExit: if no configuration was found, in this case a placeholder config is created
        ValueError: if the configuration wasn't updated after first run

    Returns:
        Config: a config object with loaded values
    """
    if not CONFIG_FILEPATH.exists():
        logger.info("no configuration found, creating an empty configuration")
        logger.info("saving empty config")
        _save_config(Config.first_use())
        raise SystemExit(
            f"please open {CONFIG_FILEPATH} and replace all the required fields, then re-run the project!"
        )
    with CONFIG_FILEPATH.open("r") as f:
        config_dict = yaml.load(f, yaml.FullLoader)

    if config_dict == asdict(Config.first_use()):
        raise SystemExit(
            f"please update your config.yaml file located at {CONFIG_FILEPATH}"
        )

    return Config.from_dict(config_dict)


def _edit_firewall_rules(config: Config, action: FirewallRuleActions) -> None:
    """
    edits the firewall rules indicated in the input config, using the input action

    Args:
        config (Config): input config object
        action (FirewallRuleActions): action to take for updating the firewalls
    """

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

    for port in config.ports:
        _edit_firewall_rule(
            config.firewall_id, config.protocol, port, config.last_ip, action
        )


def _build_rule(protocol: str, port: int, address: str) -> str:
    """
    builds a rule string to use when updating a firewall

    Args:
        protocol (str): protocol to use
        port (int): port to use
        address (str): ip address to use

    Returns:
        str: formatted string to use when sending the api request
    """
    return f"protocol:{protocol},ports:{port},address:{address}"


def _get_public_ip(max_retries: int = 3) -> str:
    """
    tries to get the public ip of the client

    Args:
        max_retries (int, optional): number of max retries to do before failing. Defaults to 3.

    Raises:
        ValueError: if the public ip couldn't be gathered

    Returns:
        str: new ip
    """
    for _ in range(max_retries):
        new_ip = requests.get(IP_PROVIDER_URL).text
        try:
            IP(new_ip)
            return new_ip
        except ValueError:
            pass
    raise ValueError(f"cannot get new ip from {IP_PROVIDER_URL}")


def _update_config(config: Config, new_ip: str) -> None:
    """
    updates the config object with the new ip. new_ip is stored in last_ip field,
    and the current last_ip is moved in the past_ips list

    Args:
        config (Config): config object
        new_ip (str): new ip to set as last ip

    Raises:
        ValueError: if new_ip is not an IP
    """
    assert isinstance(config, Config)

    try:
        IP(new_ip)
    except ValueError:
        raise ValueError(f"{new_ip} is not an IP")

    if config.last_ip != "":
        config.past_ips.append(config.last_ip)
    config.last_ip = new_ip


def _save_config(config: Config) -> None:
    """
    saves the config object to file

    Args:
        config (Config): config object
    """
    assert isinstance(config, Config)

    with CONFIG_FILEPATH.open("w") as f:
        yaml.dump(asdict(config), f)
