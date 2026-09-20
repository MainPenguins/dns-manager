from gi.repository import Gtk, Adw


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

        self.primary_entry = Adw.EntryRow(
            title="Primary DNS",
        )

        self.secondary_entry = Adw.EntryRow(
            title="Secondary DNS",
        )

        group.add(self.name_entry)
        group.add(self.primary_entry)
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

        self.parent_window.add_custom_dns(
            name,
            primary,
            secondary,
        )

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
