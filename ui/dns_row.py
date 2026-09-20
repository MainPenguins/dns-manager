from gi.repository import Gtk, Adw


class DNSRow(Adw.ActionRow):

    def __init__(
        self,
        dns,
        radio_group,
        on_selected,
        on_delete=None,
    ):
        super().__init__()

        self.dns = dns

        self.set_title(dns.name)

        subtitle = dns.primary

        if dns.secondary:
            subtitle += f"  •  {dns.secondary}"

        self.set_subtitle(subtitle)

        self.radio = Gtk.CheckButton()

        if radio_group is not None:
            self.radio.set_group(radio_group)

        self.radio.set_valign(Gtk.Align.CENTER)

        self.radio.connect(
            "toggled",
            on_selected,
            dns,
        )

        self.add_prefix(self.radio)

        if dns.custom and on_delete:
            delete_button = Gtk.Button()

            delete_button.set_icon_name(
                "user-trash-symbolic"
            )

            delete_button.set_valign(
                Gtk.Align.CENTER
            )

            delete_button.add_css_class("flat")
            delete_button.set_tooltip_text("Remove DNS")

            delete_button.connect(
                "clicked",
                on_delete,
                dns,
                self,
            )

            self.add_suffix(delete_button)
