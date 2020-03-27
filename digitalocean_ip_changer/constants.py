from pathlib import Path

ROOT_FOLDER = Path(__file__).resolve().parents[1]

IP_PROVIDER_URL = "https://api.ipify.org"
CONFIG_FILEPATH = ROOT_FOLDER / "config.yaml"
LOG_FILEPATH = ROOT_FOLDER / "digitalocean_ip_changer.log"
