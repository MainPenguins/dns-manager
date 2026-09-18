# This module detects where is resolv.conf and what is this file linked to

from pathlib import Path


def get_resolv_conf_info():
    path = Path("/etc/resolv.conf")

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
