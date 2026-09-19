# BooOOOooooOooOOOOoooOOooOO, asamiwr
import sys
import json
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw


APP_ID = "com.example.DNSChanger"

CONFIG_DIR = Path.home() / ".config" / "dns-changer"
CONFIG_FILE = CONFIG_DIR / "dns.json"

DEFAULT_DNS = [
    {
        "name": "Google",
        "address": "8.8.8.8",
        "secondary": "8.8.4.4",
    },
    {
        "name": "Cloudflare",
        "address": "1.1.1.1",
        "secondary": "1.0.0.1",
    },
    {
        "name": "Quad9",
        "address": "9.9.9.9",
        "secondary": "149.112.112.112",
    },
    {
        "name": "AdGuard",
        "address": "94.140.14.14",
        "secondary": "94.140.15.15",
    },
    {
        "name": "OpenDNS",
        "address": "208.67.222.222",
        "secondary": "208.67.220.220",
    },
]


class AddDNSDialog(Adw.Dialog):

    def __init__(self, parent):
        super().__init__()

        self.parent_window = parent

        self.set_title("Add DNS")
        self.set_content_width(450)
        self.set_content_height(400)

        toolbar_view = Adw.ToolbarView()

        header = Adw.HeaderBar()
        toolbar_view.add_top_bar(header)

        content = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=18,
        )

        content.set_margin_top(24)
        content.set_margin_bottom(24)
        content.set_margin_start(24)
        content.set_margin_end(24)

        title = Gtk.Label(
            label="Add a custom DNS server",
        )

        title.add_css_class("title-2")
        title.set_halign(Gtk.Align.START)

        content.append(title)

        description = Gtk.Label(
            label="Add your own DNS server to the list.",
        )

        description.set_wrap(True)
        description.set_xalign(0)
        description.add_css_class("dim-label")

        content.append(description)

        group = Adw.PreferencesGroup()

        self.name_entry = Adw.EntryRow(
            title="Name",
        )

        group.add(self.name_entry)

        self.primary_entry = Adw.EntryRow(
            title="Primary DNS",
        )

        group.add(self.primary_entry)

        self.secondary_entry = Adw.EntryRow(
            title="Secondary DNS",
        )

        group.add(self.secondary_entry)

        content.append(group)

        add_button = Gtk.Button(
            label="Add DNS",
        )

        add_button.add_css_class("suggested-action")
        add_button.add_css_class("pill")
        add_button.set_halign(Gtk.Align.END)

        add_button.connect(
            "clicked",
            self.on_add_clicked,
        )

        content.append(add_button)

        toolbar_view.set_content(content)

        self.set_child(toolbar_view)

    def on_add_clicked(self, button):
        name = self.name_entry.get_text().strip()
        primary = self.primary_entry.get_text().strip()
        secondary = self.secondary_entry.get_text().strip()

        if not name or not primary:
            self.show_error(
                "Please enter a name and a primary DNS address."
            )
            return

        dns = {
            "name": name,
            "address": primary,
            "secondary": secondary,
            "custom": True,
        }

        self.parent_window.add_custom_dns(dns)
        self.close()

    def show_error(self, message):
        dialog = Adw.AlertDialog(
            heading="Invalid DNS",
            body=message,
        )

        dialog.add_response(
            "ok",
            "OK",
        )

        dialog.set_default_response("ok")
        dialog.present(self)


class MainWindow(Adw.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title("DNS Changer")
        self.set_default_size(650, 700)

        self.custom_dns = self.load_dns()
        self.radio_group = None

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

        default_group.set_title(
            "Default DNS servers"
        )

        default_group.set_description(
            "Choose a DNS server to use."
        )

        page.add(default_group)

        for dns in DEFAULT_DNS:
            row = self.create_dns_row(
                dns,
                custom=False,
            )

            default_group.add(row)

        if self.custom_dns:
            self.custom_group = Adw.PreferencesGroup()

            self.custom_group.set_title(
                "Custom DNS servers"
            )

            self.custom_group.set_description(
                "DNS servers you've added yourself."
            )

            page.add(self.custom_group)

            for dns in self.custom_dns:
                row = self.create_dns_row(
                    dns,
                    custom=True,
                )

                self.custom_group.add(row)

        else:
            self.custom_group = None

        info_group = Adw.PreferencesGroup()

        info_group.set_title(
            "DNS Changer"
        )

        info_group.set_description(
            "Select a DNS server from the list above."
        )

        page.add(info_group)

        scrolled.set_child(page)

        toolbar_view.set_content(scrolled)

        self.set_content(toolbar_view)

    def create_dns_row(self, dns, custom=False):
        row = Adw.ActionRow()

        row.set_title(dns["name"])

        subtitle = dns["address"]

        if dns.get("secondary"):
            subtitle += f"  •  {dns['secondary']}"

        row.set_subtitle(subtitle)

        radio = Gtk.CheckButton()

        if self.radio_group is not None:
            radio.set_group(self.radio_group)
        else:
            self.radio_group = radio

        radio.set_valign(Gtk.Align.CENTER)

        radio.connect(
            "toggled",
            self.on_dns_selected,
            dns,
        )

        row.add_prefix(radio)

        if custom:
            delete_button = Gtk.Button()

            delete_button.set_icon_name(
                "user-trash-symbolic"
            )

            delete_button.set_valign(
                Gtk.Align.CENTER
            )

            delete_button.add_css_class("flat")

            delete_button.set_tooltip_text(
                "Remove DNS"
            )

            delete_button.connect(
                "clicked",
                self.delete_custom_dns,
                dns,
                row,
            )

            row.add_suffix(delete_button)

        return row

    def on_dns_selected(self, button, dns):
        if not button.get_active():
            return

        print(
            f"Selected DNS: {dns['name']} "
            f"({dns['address']})"
        )

    def open_add_dns_dialog(self, button):
        dialog = AddDNSDialog(self)
        dialog.present(self)

    def add_custom_dns(self, dns):
        self.custom_dns.append(dns)

        self.save_dns()

        if self.custom_group is None:
            toolbar_view = self.get_content()
            scrolled = toolbar_view.get_content()
            page = scrolled.get_child()

            self.custom_group = Adw.PreferencesGroup()

            self.custom_group.set_title(
                "Custom DNS servers"
            )

            self.custom_group.set_description(
                "DNS servers you've added yourself."
            )

            page.add(self.custom_group)

        row = self.create_dns_row(
            dns,
            custom=True,
        )

        self.custom_group.add(row)

    def delete_custom_dns(self, button, dns, row):
        self.custom_dns.remove(dns)

        self.save_dns()

        row.get_parent().remove(row)

    def save_dns(self):
        CONFIG_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        with CONFIG_FILE.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.custom_dns,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def load_dns(self):
        if not CONFIG_FILE.exists():
            return []

        try:
            with CONFIG_FILE.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            if isinstance(data, list):
                return data

        except (
            OSError,
            json.JSONDecodeError,
        ):
            pass

        return []


class DNSChanger(Adw.Application):

    def __init__(self, **kwargs):
        super().__init__(
            application_id=APP_ID,
            **kwargs,
        )

        self.connect(
            "activate",
            self.on_activate,
        )

    def on_activate(self, app):
        self.window = MainWindow(
            application=app
        )

        self.window.present()


app = DNSChanger()
app.run(sys.argv)
