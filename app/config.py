import json
from pathlib import Path

from app.models import DNSServer


CONFIG_DIR = Path.home() / ".config" / "dns-manager"
CONFIG_FILE = CONFIG_DIR / "dns-list.json"


class ConfigManager:

    def load_dns(self):
        if not CONFIG_FILE.exists():
            return []

        try:
            with CONFIG_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                return []

            return [
                DNSServer(
                    name=dns["name"],
                    primary=dns["primary"],
                    secondary=dns.get("secondary"),
                    custom=True,
                )
                for dns in data
            ]

        except (
            OSError,
            json.JSONDecodeError,
            KeyError,
            TypeError,
        ):
            return []

    def save_dns(self, dns_servers):
        CONFIG_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = [
            {
                "name": dns.name,
                "primary": dns.primary,
                "secondary": dns.secondary,
            }
            for dns in dns_servers
        ]

        with CONFIG_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )
