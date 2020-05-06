"""
constants used in the project
"""
from pathlib import Path

ROOT_FOLDER = Path(__file__).resolve().parents[1]
PROJECT_NAME = "digitalocean_firewalls_ip_changer"

PROJECT_FOLDER = ROOT_FOLDER / PROJECT_NAME

if ROOT_FOLDER.name == "site-packages":
    ROOT_FOLDER = Path(Path.home() / ("." + PROJECT_NAME))
    if not ROOT_FOLDER.exists():
        ROOT_FOLDER.mkdir(parents=True)

IP_PROVIDER_URL = "https://api.ipify.org"
CONFIG_FILEPATH = ROOT_FOLDER / "config.yaml"

LOGS_FOLDER = ROOT_FOLDER / "logs"
LOG_FILEPATH = LOGS_FOLDER / (PROJECT_NAME + ".log")
