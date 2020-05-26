"""
configuration object used to serialize and deserialize user data
"""
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

import marshmallow_dataclass
from IPy import IP
from marshmallow import ValidationError
from marshmallow.validate import Validator
from marshmallow_dataclass import NewType

from digitalocean_firewalls_ip_changer.errors import BadConfigInputError

logger = logging.getLogger(__name__)


class IPValidator(Validator):
    def __call__(self, value: Any) -> Any:
        try:
            IP(value)
        except ValueError:
            raise ValidationError("not an IP")
        return value


class ListOfPortsValidator(Validator):
    def __call__(self, values: Any) -> Any:
        if not isinstance(values, list):
            raise ValidationError("not a list")

        for value in values:
            if not isinstance(value, int):
                raise ValidationError("not an int")

            if not value > 0:
                raise ValidationError("port not > 0")
        return values


IPType = NewType("IP", str, validate=IPValidator())


@dataclass
class Config:
    """
    config class storing parameters
    """

    firewall_id: str
    last_ip: IPType  # type: ignore
    past_ips: List[IPType]  # type: ignore
    ports: List[int] = field(metadata={"validate": ListOfPortsValidator()})
    protocol: str

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
            firewall_id="replace this with your firewall id",
            last_ip="",
            past_ips=[],
            ports=[-1],
            protocol="tcp",
        )


ConfigSchema = marshmallow_dataclass.class_schema(Config)
