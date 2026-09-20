from app.backends.systemd_resolved import SystemdResolved
from app.config import ConfigManager
from app.models import DNSServer
from app.resolver import Resolver


class DNSService:

    def __init__(self):
        self.resolver = Resolver()
        self.config = ConfigManager()
        self.systemd_resolved = SystemdResolved()

    def get_custom_dns(self):
        return self.config.load_dns()

    def save_custom_dns(self, dns_servers):
        self.config.save_dns(dns_servers)

    def get_backend(self):
        return self.resolver.get_backend()

    def apply_dns(self, dns):
        backend = self.resolver.get_backend()

        if backend != "systemd-resolved":
            raise RuntimeError(
                f"Unsupported DNS backend: {backend}"
            )

        interface = self.systemd_resolved.get_default_interface()

        if interface is None:
            raise RuntimeError(
                "Could not find the default network interface."
            )

        self.systemd_resolved.set_dns(
            interface,
            dns.primary,
            dns.secondary,
        )

    def reset_dns(self):
        backend = self.resolver.get_backend()

        if backend != "systemd-resolved":
            raise RuntimeError(
                f"Unsupported DNS backend: {backend}"
            )

        interface = self.systemd_resolved.get_default_interface()

        if interface is None:
            raise RuntimeError(
                "Could not find the default network interface."
            )

        self.systemd_resolved.reset_dns(interface)
