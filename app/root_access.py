import subprocess
from . import detect

def take_root_access():
    resolv_conf_path = detect.get_resolv_conf_info()["real_path"]
    print(f"resolv_conf_path: {resolv_conf_path}")

    result = subprocess.run(
        ["pkexec", "id"],
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    print(result.stderr)
