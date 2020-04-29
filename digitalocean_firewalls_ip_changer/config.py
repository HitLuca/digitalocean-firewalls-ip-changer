"""
configuration object used to serialize and deserialize user data
"""
import logging

from dataclasses import dataclass
from IPy import IP

logger = logging.getLogger(__name__)


@dataclass
class Config:
    firewall_id: str
    last_ip: str
    past_ips: list
    ports: list
    protocol: str

    @staticmethod
    def from_dict(config: dict) -> "Config":
        """
        parses an input config dictionary into a config object

        Raises:
            ValueError: if last_ip is not an ip
            ValueError: if one of the past_ips is not an ip

        Returns:
            Config: config object
        """
        assert isinstance(config, dict), f"{type(config)}"

        keys_list = ["firewall_id", "last_ip", "past_ips", "ports", "protocol"]
        config_keys = list(config.keys())

        assert set(keys_list) == set(
            config_keys
        ), f"expected config to have keys {keys_list}, got {config_keys}"

        firewall_id = config["firewall_id"]
        last_ip = config["last_ip"]
        past_ips = config["past_ips"]
        ports = config["ports"]
        protocol = config["protocol"]

        assert isinstance(firewall_id, str)

        assert isinstance(last_ip, str)
        if last_ip != "":
            try:
                IP(last_ip)
            except ValueError:
                raise ValueError(f"{last_ip} is not an IP")

        assert isinstance(past_ips, list)
        for ip in past_ips:
            assert isinstance(ip, str)
            try:
                IP(ip)
            except ValueError:
                raise ValueError(f"{ip} is not an IP")

        assert isinstance(ports, list)

        for port in ports:
            assert isinstance(port, int)
            assert port > 0

        assert protocol == "tcp", f"{protocol}"

        config = Config(
            firewall_id=firewall_id,
            last_ip=last_ip,
            past_ips=past_ips,
            ports=ports,
            protocol=protocol,
        )
        logger.debug(config)
        return config

    @staticmethod
    def first_use() -> "Config":
        """
        returns a placeholder config for first time use

        Returns:
            Config: config object
        """
        return Config(
            firewall_id="replace this with your firewall id",
            last_ip="",
            past_ips=[],
            ports=["replace this with a list of ports to apply rules to"],
            protocol="tcp",
        )
