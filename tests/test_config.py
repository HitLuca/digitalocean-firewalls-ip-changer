import pytest
from dataclasses import asdict

from digitalocean_firewalls_ip_changer.config import Config


@pytest.fixture(name="empty_config")
def fixture_empty_config() -> dict:
    return {
        "firewall_id": "",
        "last_ip": "",
        "past_ips": [],
        "ports": [],
        "protocol": "",
    }


def test__from_dict__not_dict():
    config = "test"

    with pytest.raises(AssertionError, match=f"{type(config)}"):
        Config.from_dict(config)


def test__from_dict__missing_keys():
    config = {"firewall_id": ""}

    with pytest.raises(
        AssertionError,
        match=f"expected config to have keys ['firewall_id', 'last_ip', 'past_ips', 'ports', 'protocol', got ['firewall_id']",
    ):
        Config.from_dict(config)


def test__from_dict__wrong_types(empty_config):
    config = dict(empty_config)
    config["firewall_id"] = 3
    with pytest.raises(AssertionError):
        Config.from_dict(config)

    config = dict(empty_config)
    config["last_ip"] = 3
    with pytest.raises(AssertionError):
        Config.from_dict(config)

    config = dict(empty_config)
    ip = "123.123.w.12"
    config["last_ip"] = ip
    with pytest.raises(ValueError, match=f"{ip} is not an IP"):
        Config.from_dict(config)

    empty_config["last_ip"] = "192.168.0.1"

    config = dict(empty_config)
    config["past_ips"] = 3
    with pytest.raises(AssertionError):
        Config.from_dict(config)

    config = dict(empty_config)
    config["past_ips"] = [3]
    with pytest.raises(AssertionError):
        Config.from_dict(config)

    config = dict(empty_config)
    ip = "test.123.12.gest"
    config["past_ips"] = [ip]
    with pytest.raises(ValueError, match=f"{ip} is not an IP"):
        Config.from_dict(config)

    config = dict(empty_config)
    config["ports"] = 3
    with pytest.raises(AssertionError):
        Config.from_dict(config)

    config = dict(empty_config)
    config["ports"] = ["3"]
    with pytest.raises(AssertionError):
        Config.from_dict(config)

    config = dict(empty_config)
    config["ports"] = [-3]
    with pytest.raises(AssertionError):
        Config.from_dict(config)

    config = dict(empty_config)
    config["protocol"] = 3
    with pytest.raises(AssertionError):
        Config.from_dict(config)


def test__from_dict(empty_config):
    empty_config["firewall_id"] = "test"
    empty_config["last_ip"] = "192.168.0.1"
    empty_config["past_ips"] = ["192.168.3.1", "192.232.0.1"]
    empty_config["ports"] = [1, 50, 332]
    empty_config["protocol"] = "tcp"

    Config.from_dict(empty_config)


def test__first_use():
    assert asdict(Config.first_use()) == {
        "firewall_id": "replace this with your firewall id",
        "last_ip": "",
        "past_ips": [],
        "ports": ["replace this with a list of ports to apply rules to"],
        "protocol": "tcp",
    }
