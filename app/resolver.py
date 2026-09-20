from pathlib import Path


class Resolver:

    def __init__(self):
        self.resolv_conf = Path("/etc/resolv.conf")

    def get_info(self):
        path = self.resolv_conf

        if not path.exists() and not path.is_symlink():
            return {
                "exists": False,
                "is_symlink": False,
                "target": None,
                "real_path": None,
            }

        if path.is_symlink():
            return {
                "exists": True,
                "is_symlink": True,
                "target": str(path.readlink()),
                "real_path": str(path.resolve()),
            }

        return {
            "exists": True,
            "is_symlink": False,
            "target": None,
            "real_path": str(path),
        }

    def get_resolv_conf_path(self):
        info = self.get_info()

        if not info["exists"]:
            return None

        return info["real_path"]

    def get_backend(self):
        if Path("/run/systemd/resolve").exists():
            return "systemd-resolved"

        return "unknown"
