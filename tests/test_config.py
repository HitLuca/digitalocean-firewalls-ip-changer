from dataclasses import asdict
from typing import Any, Dict

import pytest

from digitalocean_firewalls_ip_changer.config import Config
from digitalocean_firewalls_ip_changer.errors import BadConfigInputError


@pytest.fixture(name="empty_config")  # type: ignore
def fixture_empty_config() -> Dict[str, Any]:
    return {
        "firewalls": [{"firewall_id": "", "rules": [{"protocol": "", "port": 0}]}],
        "last_ip": "",
        "past_ips": [],
    }


def test__from_dict__not_dict() -> None:
    config = "test"

    with pytest.raises(AssertionError, match=f"{type(config)}"):
        Config.from_dict(config)  # type: ignore


def test__from_dict__missing_keys() -> None:
    config = {"last_ip": ""}

    with pytest.raises(BadConfigInputError):
        Config.from_dict(config)


def test__from_dict__wrong_types(empty_config: Dict[str, Any]) -> None:
    config = dict(empty_config)
    config["firewalls"][0]["firewall_id"] = 3
    with pytest.raises(BadConfigInputError):
        Config.from_dict(config)

    config = dict(empty_config)
    config["last_ip"] = 3
    with pytest.raises(BadConfigInputError):
        Config.from_dict(config)

    config = dict(empty_config)
    ip = "123.123.w.12"
    config["last_ip"] = ip
    with pytest.raises(BadConfigInputError):
        Config.from_dict(config)

    empty_config["last_ip"] = "192.168.0.1"

    config = dict(empty_config)
    config["past_ips"] = 3
    with pytest.raises(BadConfigInputError):
        Config.from_dict(config)

    config = dict(empty_config)
    config["past_ips"] = [3]
    with pytest.raises(BadConfigInputError):
        Config.from_dict(config)

    config = dict(empty_config)
    ip = "test.123.12.gest"
    config["past_ips"] = [ip]
    with pytest.raises(BadConfigInputError):
        Config.from_dict(config)

    config = dict(empty_config)
    config["firewalls"][0]["rules"][0]["port"] = 3
    with pytest.raises(BadConfigInputError):
        Config.from_dict(config)

    config = dict(empty_config)
    config["firewalls"][0]["rules"][0]["port"] = "3a"
    with pytest.raises(BadConfigInputError):
        Config.from_dict(config)

    config = dict(empty_config)
    config["firewalls"][0]["rules"][0]["port"] = -3
    with pytest.raises(BadConfigInputError):
        Config.from_dict(config)

    config = dict(empty_config)
    config["firewalls"][0]["rules"][0]["protocol"] = 3
    with pytest.raises(BadConfigInputError):
        Config.from_dict(config)


def test__from_dict(empty_config: Dict[str, Any]) -> None:
    empty_config["firewalls"][0]["firewall_id"] = "test"
    empty_config["last_ip"] = "192.168.0.1"
    empty_config["past_ips"] = ["192.168.3.1", "192.111.0.1"]
    empty_config["firewalls"][0]["rules"][0]["port"] = 1
    empty_config["firewalls"][0]["rules"][0]["protocol"] = "tcp"

    Config.from_dict(empty_config)


def test__first_use() -> None:
    assert asdict(Config.first_use()) == {
        "firewalls": [
            {
                "firewall_id": "replace this with your firewall id",
                "rules": [{"protocol": "tcp", "port": 0}],
            }
        ],
        "last_ip": "",
        "past_ips": [],
    }
