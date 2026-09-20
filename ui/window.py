from gi.repository import Gtk, Adw

from app.models import DNSServer
from data.default_dns import DEFAULT_DNS
from ui.add_dns_dialog import AddDNSDialog
from ui.dns_row import DNSRow


class MainWindow(Adw.ApplicationWindow):

    def __init__(self, dns_service, **kwargs):
        super().__init__(**kwargs)

        self.dns_service = dns_service
        self.custom_dns = self.dns_service.get_custom_dns()

        self.radio_group = None
        self.selected_dns = None

        self.set_title("DNS Manager")
        self.set_default_size(650, 700)

        self.build_ui()

    def build_ui(self):
        toolbar_view = Adw.ToolbarView()

        header = Adw.HeaderBar()

        add_button = Gtk.Button()
        add_button.set_icon_name("list-add-symbolic")
        add_button.set_tooltip_text("Add custom DNS")
        add_button.add_css_class("suggested-action")

        add_button.connect(
            "clicked",
            self.open_add_dns_dialog,
        )

        header.pack_end(add_button)

        toolbar_view.add_top_bar(header)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)

        page = Adw.PreferencesPage()

        default_group = Adw.PreferencesGroup()
        default_group.set_title("Default DNS servers")
        default_group.set_description(
            "Choose a DNS server to use."
        )

        page.add(default_group)

        for dns in DEFAULT_DNS:
            row = self.create_dns_row(dns)
            default_group.add(row)

        if self.custom_dns:
            self.custom_group = self.create_custom_group()

            for dns in self.custom_dns:
                row = self.create_dns_row(dns)
                self.custom_group.add(row)

            page.add(self.custom_group)

        else:
            self.custom_group = None

        apply_group = Adw.PreferencesGroup()

        apply_group.set_title("Apply DNS")
        apply_group.set_description(
            "Apply the selected DNS server to your system."
        )

        self.apply_button = Gtk.Button(
            label="Apply DNS",
        )

        self.apply_button.add_css_class(
            "suggested-action"
        )

        self.apply_button.add_css_class("pill")

        self.apply_button.set_sensitive(False)

        self.apply_button.connect(
            "clicked",
            self.on_apply_dns,
        )

        apply_group.add(self.apply_button)

        page.add(apply_group)

        scrolled.set_child(page)
        toolbar_view.set_content(scrolled)

        self.set_content(toolbar_view)

    def create_custom_group(self):
        group = Adw.PreferencesGroup()

        group.set_title("Custom DNS servers")
        group.set_description(
            "DNS servers you've added yourself."
        )

        return group

    def create_dns_row(self, dns):
        row = DNSRow(
            dns=dns,
            radio_group=self.radio_group,
            on_selected=self.on_dns_selected,
            on_delete=self.delete_custom_dns
            if dns.custom
            else None,
        )

        if self.radio_group is None:
            self.radio_group = row.radio

        return row

    def on_dns_selected(self, button, dns):
        if not button.get_active():
            return

        self.selected_dns = dns
        self.apply_button.set_sensitive(True)

        print(
            f"Selected DNS: {dns.name} "
            f"({dns.primary})"
        )

    def on_apply_dns(self, button):
        if self.selected_dns is None:
            return

        try:
            self.dns_service.apply_dns(
                self.selected_dns
            )

            self.show_message(
                "DNS applied",
                f"{self.selected_dns.name} is now active.",
            )

        except RuntimeError as error:
            self.show_message(
                "Failed to apply DNS",
                str(error),
            )

    def show_message(self, heading, body):
        dialog = Adw.AlertDialog(
            heading=heading,
            body=body,
        )

        dialog.add_response(
            "ok",
            "OK",
        )

        dialog.set_default_response("ok")
        dialog.present(self)

    def open_add_dns_dialog(self, button):
        dialog = AddDNSDialog(self)
        dialog.present(self)

    def add_custom_dns(self, name, primary, secondary):
        dns = DNSServer(
            name=name,
            primary=primary,
            secondary=secondary or None,
            custom=True,
        )

        self.custom_dns.append(dns)

        self.dns_service.save_custom_dns(
            self.custom_dns
        )

        if self.custom_group is None:
            self.custom_group = self.create_custom_group()
            self.page.add(self.custom_group)

        row = self.create_dns_row(dns)
        self.custom_group.add(row)

    def delete_custom_dns(self, button, dns, row):
        if self.selected_dns is dns:
            self.selected_dns = None
            self.apply_button.set_sensitive(False)

        self.custom_dns.remove(dns)

        self.dns_service.save_custom_dns(
            self.custom_dns
        )

        row.get_parent().remove(row)
