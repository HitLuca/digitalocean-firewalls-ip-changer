"""
configuration object used to serialize and deserialize user data
"""
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

import marshmallow_dataclass
import marshmallow
from IPy import IP
from marshmallow import ValidationError
from marshmallow.validate import Validator
from marshmallow_dataclass import NewType

from digitalocean_firewalls_ip_changer.errors import BadConfigInputError

logger = logging.getLogger(__name__)


class IPValidator(Validator):
    """
    validator for strings containing IPs
    """

    def __call__(self, value: Any) -> Any:
        try:
            IP(value)
        except ValueError:
            raise ValidationError("not an IP")
        return value


IPType = NewType("IP", str, validate=IPValidator())


@dataclass
class FirewallRule:
    """
    dataclass for a firewall rule
    """

    protocol: str
    port: int = field(metadata={"validate": marshmallow.validate.Range(min=1)})


@dataclass
class FirewallConfig:
    """
    dataclass for a firewall config
    """

    firewall_id: str
    rules: List[FirewallRule]


@dataclass
class Config:
    """
    config class storing parameters
    """

    firewalls: List[FirewallConfig]
    last_ip: IPType  # type: ignore
    past_ips: List[IPType]  # type: ignore

    @staticmethod
    def from_dict(config: Dict[str, Any]) -> "Config":
        """
        loads a config from an input dictionary

        Returns:
            Config: config object
        """
        assert isinstance(config, dict), f"{type(config)}"

        try:
            config_object = ConfigSchema().load(config)
        except ValidationError as e:
            raise BadConfigInputError(e)

        assert isinstance(config_object, Config)
        return config_object

    @staticmethod
    def first_use() -> "Config":
        """
        returns a placeholder config for first time use

        Returns:
            Config: config object
        """
        return Config(
            firewalls=[
                FirewallConfig(
                    firewall_id="replace this with your firewall id",
                    rules=[FirewallRule(protocol="tcp", port=0)],
                )
            ],
            last_ip="",
            past_ips=[],
        )


ConfigSchema = marshmallow_dataclass.class_schema(Config)
