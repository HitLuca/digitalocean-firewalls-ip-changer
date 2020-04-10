from pathlib import Path

ROOT_FOLDER = Path(__file__).resolve().parents[1]

PROJECT_FOLDER = ROOT_FOLDER / "ucl_firewalls_ip_changer"

if ROOT_FOLDER.name == "site-packages":
    ROOT_FOLDER = Path(Path.home() / ".ucl_firewalls_ip_changer")
    if not ROOT_FOLDER.exists():
        ROOT_FOLDER.mkdir(parents=True)

IP_PROVIDER_URL = "https://api.ipify.org"
CONFIG_FILEPATH = ROOT_FOLDER / "config.yaml"
LOG_FILEPATH = ROOT_FOLDER / "ucl_firewalls_ip_changer.log"
