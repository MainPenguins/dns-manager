from app.models import DNSServer


DEFAULT_DNS = [
    DNSServer(
        name="Google",
        primary="8.8.8.8",
        secondary="8.8.4.4",
    ),
    DNSServer(
        name="Cloudflare",
        primary="1.1.1.1",
        secondary="1.0.0.1",
    ),
    DNSServer(
        name="Quad9",
        primary="9.9.9.9",
        secondary="149.112.112.112",
    ),
    DNSServer(
        name="AdGuard",
        primary="94.140.14.14",
        secondary="94.140.15.15",
    ),
    DNSServer(
        name="OpenDNS",
        primary="208.67.222.222",
        secondary="208.67.220.220",
    ),
]
