import subprocess


class SystemdResolved:

    def get_status(self):
        result = subprocess.run(
            ["resolvectl", "status"],
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout

    def get_default_interface(self):
        result = subprocess.run(
            ["ip", "route", "show", "default"],
            capture_output=True,
            text=True,
            check=True,
        )

        for line in result.stdout.splitlines():
            parts = line.split()

            if "dev" in parts:
                return parts[parts.index("dev") + 1]

        return None

    def set_dns(self, interface, primary, secondary=None):
        command = [
            "pkexec",
            "resolvectl",
            "dns",
            interface,
            primary,
        ]

        if secondary:
            command.append(secondary)

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip() or "Failed to change DNS."
            )

    def reset_dns(self, interface):
        result = subprocess.run(
            [
                "pkexec",
                "resolvectl",
                "revert",
                interface,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip() or "Failed to reset DNS."
            )
