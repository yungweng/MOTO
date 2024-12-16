import gi
from typing import Optional
import requests
import logging

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class Colors:
    """Color constants from CSS"""
    BACKGROUND = "#f6f4f3"
    FONT = "#1b2021"
    SELECT_BUTTON = "#BAD87A"
    INPUT_BG = "rgba(217, 217, 217, 0.5)"
    ERROR = "#DE675F"

class CreateActivityWindow(Gtk.Box):
    def __init__(self, parent_window: Gtk.Window, room_id: str) -> None:
        super().__init__(homogeneous=False, spacing=20)
        self.set_orientation(Gtk.Orientation.VERTICAL)

        self.parent_window = parent_window
        self.room_id = room_id
        self.logger = logging.getLogger(__name__)

        self._init_ui()
        self._apply_styles()
        self.show_all()

    def _init_ui(self) -> None:
        # Container margins
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        # Header with back button and help
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        # Back button
        back_button = Gtk.Button(label="Zurück")
        back_button.set_name("back_button")
        back_button.connect("clicked", self._on_back_clicked)
        header_box.pack_start(back_button, False, False, 0)

        # Help button
        help_button = Gtk.Button(label="Hilfe")
        help_button.set_name("help_button")
        help_button.connect("clicked", self._show_help_dialog)
        header_box.pack_end(help_button, False, False, 0)

        self.pack_start(header_box, False, False, 0)

        # Title and subtitle
        title = Gtk.Label()
        title.set_markup(f"<span size='24000'>Raum {self.room_id}</span>")
        title.set_name("heading_2")
        title.set_halign(Gtk.Align.START)
        self.pack_start(title, False, False, 0)


        # Title and subtitle
        title = Gtk.Label()
        #title.set_markup(f"<span size='24000'>Raum XXX</span>")  # Room number will be set later
        title.set_name("heading_2")
        title.set_halign(Gtk.Align.START)
        self.pack_start(title, False, False, 0)

        subtitle = Gtk.Label(label="Geben Sie folgende Informationen an:")
        subtitle.set_name("subheading_2")
        subtitle.set_halign(Gtk.Align.START)
        self.pack_start(subtitle, False, False, 0)

        # Form container
        form_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        form_box.set_margin_top(50)

        # Supervisor (Aufsichtsperson)
        supervisor_box = self._create_input_block(
            "Aufsichtsperson:",
            is_dropdown=True,
            options=["Person 1", "Person 2"]  # Will be populated from API
        )
        form_box.pack_start(supervisor_box, False, False, 0)

        # Activity name
        self.activity_entry = Gtk.Entry()
        self.activity_entry.set_name("inputfield")
        self.activity_entry.set_placeholder_text("Aktivitätsname")
        activity_box = self._create_input_block(
            "Aktivitätsname:",
            entry=self.activity_entry
        )
        form_box.pack_start(activity_box, False, False, 0)

        # Activity category
        category_box = self._create_input_block(
            "AG-Kategorie:",
            is_dropdown=True,
            options=["Sport", "Kunst", "Musik"]  # Will be populated from API
        )
        form_box.pack_start(category_box, False, False, 0)

        # Maximum participants
        self.capacity_entry = Gtk.Entry()
        self.capacity_entry.set_name("inputfield")
        self.capacity_entry.set_placeholder_text("Maximale Anzahl")
        capacity_box = self._create_input_block(
            "Maximale Kinderanzahl:",
            entry=self.capacity_entry
        )
        form_box.pack_start(capacity_box, False, False, 0)

        self.pack_start(form_box, True, True, 0)

        # Error message area
        self.error_label = Gtk.Label()
        self.error_label.set_name("error_label")
        self.pack_start(self.error_label, False, False, 0)

        # Submit button container
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        button_box.set_halign(Gtk.Align.CENTER)
        button_box.set_margin_top(30)

        submit_button = Gtk.Button(label="Auswählen")
        submit_button.set_name("submit_button")
        submit_button.connect("clicked", self._on_submit)
        button_box.pack_start(submit_button, False, False, 0)

        self.pack_end(button_box, False, False, 0)

    def _create_input_block(self, label_text: str, entry: Optional[Gtk.Entry] = None,
                            is_dropdown: bool = False, options: list = None) -> Gtk.Box:
        """Create an input block with label and either entry or dropdown"""
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.set_name("inputblock")

        # Label
        label = Gtk.Label(label=label_text)
        label.set_name("category")
        box.pack_start(label, False, False, 0)

        if is_dropdown and options:
            # Create dropdown
            combo = Gtk.ComboBoxText()
            combo.set_name("custom-select")
            combo.append_text("Bitte auswählen..")
            for option in options:
                combo.append_text(option)
            combo.set_active(0)
            box.pack_end(combo, True, True, 0)
        elif entry:
            # Use provided entry
            box.pack_end(entry, True, True, 0)

        return box

    def _apply_styles(self) -> None:
        css_provider = Gtk.CssProvider()
        css = f"""
            #heading_2 {{
                font-size: 48px;
                font-weight: bold;
                color: {Colors.FONT};
            }}
            
            #subheading_2 {{
                font-size: 32px;
                color: {Colors.FONT};
            }}
            
            #inputblock {{
                margin: 15px 0;
            }}
            
            #category {{
                font-size: 24px;
                color: {Colors.FONT};
            }}
            
            #inputfield {{
                background-color: {Colors.INPUT_BG};
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 24px;
                min-height: 50px;
                min-width: 410px;
            }}
            
            #custom-select {{
                background-color: {Colors.INPUT_BG};
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 24px;
                min-height: 50px;
                min-width: 432px;
            }}
            
            #submit_button {{
                background-color: {Colors.SELECT_BUTTON};
                color: {Colors.FONT};
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 24px;
                font-weight: 500;
                min-width: 200px;
                min-height: 60px;
            }}
            
            #back_button {{
                color: {Colors.FONT};
                font-size: 32px;
                font-weight: 600;
                background: none;
                border: none;
                margin-left: 50px;
            }}
            
            #help_button {{
                background: white;
                color: {Colors.FONT};
                border: 2px solid {Colors.FONT};
                border-radius: 45px;
                padding: 5px 15px;
                font-size: 20px;
            }}
            
            #error_label {{
                color: {Colors.ERROR};
                font-size: 18px;
                font-weight: 500;
            }}
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _on_back_clicked(self, button: Gtk.Button) -> None:
        self.parent_window.switch_page("choose_room")

    def _show_help_dialog(self, button: Gtk.Button) -> None:
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Was muss ich in diesem Anzeigefenster beachten?"
        )
        dialog.format_secondary_text(
            "In dieser Ansicht müssen sie die unten stehenden Eingabefelder ausfüllen, "
            "um eine Aktivität im Raum zu registrieren. Für Eingaben müssen Sie auf die "
            "grauen Schaltflächen klicken. Klicken Sie auf \"Abschließen\", um den "
            "Raum zu buchen."
        )
        dialog.run()
        dialog.destroy()

    def _on_submit(self, button: Gtk.Button) -> None:
        # TODO: Implement form validation and submission
        activity_name = self.activity_entry.get_text()
        capacity = self.capacity_entry.get_text()

        if not activity_name.strip():
            self.error_label.set_text("Bitte geben Sie einen Namen für die Aktivität an")
            return

        try:
            capacity_int = int(capacity)
            if capacity_int <= 0:
                self.error_label.set_text("Die maximale Kapazität muss größer als Null sein")
                return
        except ValueError:
            self.error_label.set_text("Bitte geben Sie die maximale Anzahl an Teilnehmern an")
            return

        # TODO: Add API call to create activity

    def _on_submit(self, button: Gtk.Button) -> None:
        """Handle activity creation and redirect to home"""
        activity_name = self.activity_entry.get_text()
        capacity = self.capacity_entry.get_text()

        if not activity_name.strip():
            self.error_label.set_text("Bitte geben Sie einen Namen für die Aktivität an")
            return

        try:
            capacity_int = int(capacity)
            if capacity_int <= 0:
                self.error_label.set_text("Die maximale Kapazität muss größer als Null sein")
                return
        except ValueError:
            self.error_label.set_text("Bitte geben Sie die maximale Anzahl an Teilnehmern an")
            return

        # TODO: Add API call to create activity
        # After successful creation:
        self.parent_window.switch_to_home(self.room_id)