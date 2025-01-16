import gi
from typing import Optional, List, Dict
import logging
import requests

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class Colors:
    BACKGROUND = "#f6f4f3"
    FONT = "#1b2021"
    GREEN = "#83cd2d"
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

        label1 = Gtk.Label(label="Kategorie")
        label1.set_name("header_label1")
        label1.set_xalign(0)  # Align text to the left
        header_grid.attach(label1, 0, 0, 1, 1)

        label2 = Gtk.Label(label="Aktueller Wert")
        label2.set_name("header_label2")
        label2.set_xalign(0)  # Align text to the left
        header_grid.attach(label2, 1, 0, 1, 1)

        label3 = Gtk.Label(label="Neuer Wert")
        label3.set_name("header_label3")
        label3.set_xalign(0)  # Align text to the left
        header_grid.attach(label3, 2, 0, 1, 1)

        label4 = Gtk.Label(label="")
        label4.set_name("header_label4")
        label4.set_xalign(0)  # Align text to the left
        header_grid.attach(label4, 3, 0, 1, 1)




        self.pack_start(header_grid, False, False, 20)


        self.form_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.form_box.set_name("form_container")
        self.parent_window.set_resizable(True)
        # Form container
        form_grid = Gtk.Grid()
        form_grid.set_name("form_grid")
        form_grid.set_row_spacing(30)
        form_grid.set_column_spacing(10)
        #form_grid.set_margin_top(10)
        form_grid.set_margin_start(10)
        form_grid.set_margin_end(10)

        # Supervisor (Aufsichtsperson)
        supervisor_label = Gtk.Label(label="Aufsichtsperson:")
        supervisor_label.set_name("category")
        supervisor_label.set_xalign(0)  # Align text to the left

        supervisor_current = Gtk.Label(label="Max Mustermann") # TODO: Populate from API @chris
        supervisor_current.set_name("current")

        supervisor_dropdown = Gtk.ComboBoxText()
        supervisor_dropdown.set_name("dropdown")
        supervisor_dropdown.set_hexpand(True)  # Allow it to expand in the grid
        supervisor_dropdown.append_text("Bitte auswählen...")
        supervisor_dropdown.append_text("Person 1") # TODO: Populate from API @chris
        supervisor_dropdown.append_text("Person 2")
        supervisor_dropdown.set_active(0)  # Select the first option by default

        change_button = Gtk.Button(label="Ändern")
        change_button.set_name("change_button")

        form_grid.attach(supervisor_label, 0, 0, 1, 1)  # Column 0, Row 0
        form_grid.attach(supervisor_current, 1, 0, 1, 1)  # Column 1, Row 0
        form_grid.attach(supervisor_dropdown, 2, 0, 1, 1)  # Column 2, Row 0
        form_grid.attach(change_button, 3, 0, 1, 1)  # Column 3, Row 0


        # Activity name
        activity_label = Gtk.Label(label="Aktivitätsname:")
        activity_label.set_name("category")
        activity_label.set_xalign(0)

        activity_current = Gtk.Label(label="Fußball") # TODO: Populate from API @chris
        activity_current.set_name("current")

        activity_entry = Gtk.Entry()
        activity_entry.set_placeholder_text("Aktivitätsname")
        activity_entry.set_name("inputfield")

        change_button = Gtk.Button(label="Ändern")
        change_button.set_name("change_button")

        form_grid.attach(activity_label, 0, 1, 1, 1)  # Column 0, Row 1
        form_grid.attach(activity_current, 1, 1, 1, 1)  # Column 1, Row 1
        form_grid.attach(activity_entry, 2, 1, 1, 1)  # Column 2, Row 1
        form_grid.attach(change_button, 3, 1, 1, 1)  # Column 3, Row 1

        # Activity category
        category_label = Gtk.Label(label="AG-Kategorie:")
        category_label.set_name("category")
        category_label.set_xalign(0)

        category_current = Gtk.Label(label="Sport") # TODO: Populate from API @chris
        category_current.set_name("current")

        category_dropdown = Gtk.ComboBoxText()
        category_dropdown.set_hexpand(True)
        category_dropdown.set_name("dropdown")
        category_dropdown.append_text("Bitte auswählen...")
        category_dropdown.append_text("Sport") # TODO: Populate from API @chris
        category_dropdown.append_text("Kunst")
        category_dropdown.append_text("Musik")
        category_dropdown.set_active(0)

        change_button = Gtk.Button(label="Ändern")
        change_button.set_name("change_button")

        form_grid.attach(category_label, 0, 2, 1, 1)  # Column 0, Row 2
        form_grid.attach(category_current, 1, 2, 1, 1)  # Column 1, Row 2
        form_grid.attach(category_dropdown, 2, 2, 1, 1)  # Column 2, Row 2
        form_grid.attach(change_button, 3, 2, 1, 1)  # Column 3, Row 2

        # Maximum participants
        capacity_label = Gtk.Label(label="Maximale Kinderanzahl:")
        capacity_label.set_name("category")
        capacity_label.set_xalign(0)

        capacity_current = Gtk.Label(label="20") # TODO: Populate from API
        capacity_current.set_name("current")

        capacity_entry = Gtk.Entry()
        capacity_entry.set_placeholder_text("Maximale Anzahl")
        capacity_entry.set_name("inputfield")


        change_button = Gtk.Button(label="Ändern")
        change_button.set_name("change_button")

        form_grid.attach(capacity_label, 0, 3, 1, 1)  # Column 0, Row 3
        form_grid.attach(capacity_current, 1, 3, 1, 1)  # Column 1, Row 3
        form_grid.attach(capacity_entry, 2, 3, 1, 1)  # Column 2, Row 3
        form_grid.attach(change_button, 3, 3, 1, 1)  # Column 3, Row 3

        # Add grid to the container
        self.pack_start(form_grid, True, True, 0)


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
                font-size: 32px;
                color: {Colors.FONT};
            }}
            
            #help_button {{
                font-family: "Inter", sans-serif;
                background: {Colors.HELP_BUTTON};
                color: {Colors.FONT};
                border: 2px solid {Colors.FONT};
                border-radius: 45px;
                padding: 10px 25px;
                font-family: "Inter", sans-serif;
                font-size: 20px;
                box-shadow: rgba(0, 0, 0, 0.2) 15px 28px 25px -18px;
            }}
            #help_button:hover {{
                box-shadow: rgba(0, 0, 0, 0.3) 2px 8px 8px -5px;
            }}
            
            #header_line {{
                border-bottom: 1px solid {Colors.FONT};
            }}
            
            #header_label1, #header_label2, #header_label3, #header_label4 {{
                font-family: "Inter", sans-serif;
                font-size: 24px;
                font-weight: 600;
                min-width: 250px;
                color: {Colors.FONT};
                padding: 10px;
            }}
            
            #header_label1 {{
                min-width: 260px;
            }}
            
            #header_label2 {{
                min-width: 215px;
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
            
            #dropdown {{
                font-family: "Inter", sans-serif;
                background-color: {Colors.LIST_BG};
                border-radius: 10px;
                font-size: 24px;
                color: {Colors.FONT};
                min-width: 180px;
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
                background: {Colors.GREEN};
                color: {Colors.FONT};
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 24px;
                font-weight: 600;
                min-width: 120px;
                box-shadow: rgba(0, 0, 0, 0.2) 15px 28px 25px -18px;
            }}
            #change_button:hover {{
                box-shadow: rgba(0, 0, 0, 0.3) 2px 8px 8px -5px;
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