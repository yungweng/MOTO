import gi
from typing import Optional, List, Dict
import logging
import requests

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class Colors:
    BACKGROUND = "#f6f4f3"
    FONT = "#1b2021"
    GREEN = "#BAD87A"
    LIST_BG = "rgba(217, 217, 217, 0.25)"
    LIST_LINE = "#c0c0c0"
    INPUT_BG = "rgba(217, 217, 217, 0.5)"
    HELP_BUTTON = "#ffffff"

class ChangeRoomDataWindow(Gtk.Box):
    def __init__(self, parent_window: Gtk.Window, room_id: str) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.parent_window = parent_window
        self.room_id = room_id
        self._init_ui()
        self._apply_styles()
        self._load_data()
        self.show_all()

    def _init_ui(self) -> None:
        self.set_margin_top(30)
        self.set_margin_bottom(30)
        self.set_margin_start(50)
        self.set_margin_end(50)

        # Header with back and help buttons
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        back_button = Gtk.Button(label="← Zurück")
        back_button.set_name("help_button")
        back_button.connect("clicked", lambda x: self.parent_window.switch_page("master_tablet"))
        header_box.pack_start(back_button, False, False, 0)

        help_button = Gtk.Button(label="HILFE")
        help_button.set_name("help_button")
        help_button.connect("clicked", self._show_help_dialog)
        header_box.pack_end(help_button, False, False, 0)
        self.pack_start(header_box, False, False, 0)

        # Title and subtitle
        title = Gtk.Label(label=f"Raumangaben für Raum {self.room_id}")
        title.set_name("heading")
        title.set_halign(Gtk.Align.START)
        self.pack_start(title, False, False, 0)

        subtitle = Gtk.Label(label="Ändern Sie bei Bedarf folgende Informationen:")
        subtitle.set_name("subheading")
        subtitle.set_halign(Gtk.Align.START)
        self.pack_start(subtitle, False, False, 0)

        # Header line
        header_grid = Gtk.Grid()
        header_grid.set_column_spacing(10)
        header_grid.set_name("header_line")

        labels = ["Kategorie", "Aktueller Wert", "Neuer Wert", ""]
        for i, text in enumerate(labels):
            label = Gtk.Label(label=text)
            label.set_name("header_label")
            header_grid.attach(label, i, 0, 1, 1)

        self.pack_start(header_grid, False, False, 20)

        # Form container
        self.form_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.form_box.set_margin_top(20)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.form_box)
        self.pack_start(scrolled, True, True, 0)

    def _create_form_row(self, label: str, current_value: str, is_dropdown: bool = False,
                         options: List[str] = None) -> Gtk.Box:
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.set_name("inputblock")

        # Label
        label_widget = Gtk.Label(label=label)
        label_widget.set_name("category")
        row.pack_start(label_widget, False, True, 0)

        # Current value
        current = Gtk.Label(label=current_value)
        current.set_name("current")
        row.pack_start(current, True, True, 0)

        # Input field
        if is_dropdown:
            combo = Gtk.ComboBoxText()
            combo.set_name("custom-select")
            combo.append_text("Bitte auswählen..")
            for option in (options or []):
                combo.append_text(option)
            combo.set_active(0)
            row.pack_start(combo, True, True, 0)
        else:
            entry = Gtk.Entry()
            entry.set_name("inputfield")
            entry.set_placeholder_text("Neuer Wert..")
            row.pack_start(entry, True, True, 0)

        # Change button
        button = Gtk.Button(label="Ändern")
        button.set_name("change_button")
        row.pack_end(button, False, False, 0)

        return row

    def _add_separator(self) -> None:
        separator = Gtk.Separator()
        separator.set_name("line")
        self.form_box.pack_start(separator, False, False, 10)

    def _load_data(self) -> None:
        # TODO: Replace with actual API calls
        supervisors = ["Max Mustermann", "Erika Musterfrau"]
        categories = ["Sport", "Kunst", "Musik"]
        current_data = {
            "supervisor": "Max Mustermann",
            "activity": "Fußball",
            "category": "Sport",
            "capacity": "20"
        }

        # Add supervisor rows
        supervisor_row = self._create_form_row(
            "Aufsichtsperson:",
            current_data["supervisor"],
            True,
            supervisors
        )
        self.form_box.pack_start(supervisor_row, False, False, 0)
        self._add_separator()

        # Activity name
        activity_row = self._create_form_row(
            "Aktivitätsname:",
            current_data["activity"]
        )
        self.form_box.pack_start(activity_row, False, False, 0)
        self._add_separator()

        # Category
        category_row = self._create_form_row(
            "AG-Kategorie:",
            current_data["category"],
            True,
            categories
        )
        self.form_box.pack_start(category_row, False, False, 0)
        self._add_separator()

        # Capacity
        capacity_row = self._create_form_row(
            "Kinderanzahl:",
            current_data["capacity"]
        )
        self.form_box.pack_start(capacity_row, False, False, 0)

    def _show_help_dialog(self, button: Gtk.Button) -> None:
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Was muss ich in diesem Anzeigefenster beachten?"
        )
        dialog.format_secondary_text(
            "In dieser Ansicht können Sie bei Bedarf die Rauminformationen ändern. "
            "Geben Sie hierzu Ihre neuen Daten in das entsprechende Eingabefeld ein. "
            "Tippen Sie auf \"Ändern\", um die neuen Daten zu speichern."
        )
        dialog.run()
        dialog.destroy()

    def _apply_styles(self) -> None:
        css_provider = Gtk.CssProvider()
        css = f"""
            #heading {{
                font-family: "Inter", sans-serif;
                font-size: 48px;
                font-weight: bold;
                color: {Colors.FONT};
            }}
            
            #subheading {{
                font-family: "Inter", sans-serif;
                font-size: 24px;
                color: {Colors.FONT};
            }}
            
            #help_button {{
                background: {Colors.HELP_BUTTON};
                color: {Colors.FONT};
                border: 2px solid {Colors.FONT};
                border-radius: 45px;
                padding: 10px 25px;
                font-size: 20px;
            }}
            
            #header_line {{
                border-bottom: 1px solid {Colors.FONT};
                margin-bottom: 10px;
            }}
            
            #header_label {{
                font-family: "Inter", sans-serif;
                font-size: 24px;
                font-weight: 600;
                color: {Colors.FONT};
                padding: 10px;
            }}
            
            #inputblock {{
                padding: 10px 0;
            }}
            
            #category {{
                font-family: "Inter", sans-serif;
                font-size: 24px;
                color: {Colors.FONT};
                min-width: 200px;
            }}
            
            #current {{
                font-family: "Inter", sans-serif;
                background-color: {Colors.LIST_BG};
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 24px;
                color: {Colors.FONT};
                min-width: 180px;
            }}
            
            #inputfield, #custom-select {{
                background-color: {Colors.INPUT_BG};
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 24px;
                min-width: 200px;
            }}
            
            #change_button {{
                font-family: "Inter", sans-serif;
                background-color: {Colors.GREEN};
                color: {Colors.FONT};
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 24px;
                font-weight: 500;
                min-width: 120px;
            }}
            
            #line {{
                background-color: {Colors.LIST_LINE};
                margin: 5px 0;
            }}
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )