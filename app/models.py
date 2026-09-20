from dataclasses import dataclass


@dataclass
class DNSServer:
    name: str
    primary: str
    secondary: str | None = None
    custom: bool = False
