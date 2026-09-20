from gi.repository import Adw

from app.dns_service import DNSService
from ui.window import MainWindow


APP_ID = "com.example.DNSChanger"


class DNSChanger(Adw.Application):

    def __init__(self, **kwargs):
        super().__init__(
            application_id=APP_ID,
            **kwargs,
        )

        self.dns_service = DNSService()

        self.connect(
            "activate",
            self.on_activate,
        )

    def on_activate(self, app):
        self.window = MainWindow(
            application=app,
            dns_service=self.dns_service,
        )

        self.window.present()
