import subprocess
from . import detect

def take_root_access(dns1, dns2):
    resolv_conf_path = detect.get_resolv_conf_info()["real_path"]
    print(f"resolv_conf_path: {resolv_conf_path}")

    result = subprocess.run(
        ["pkexec", "sh", "-c", f"echo 'nameserver {dns1}' > {resolv_conf_path} && echo 'nameserver {dns2}' >> {resolv_conf_path}"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    print(result.stderr)
