import gi
from typing import List, Optional, Dict
from enum import Enum
import requests
import logging

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

class RoomState(Enum):
    IDLE = "idle"
    LOADING = "loading"
    ERROR = "error"

class Colors:
    BACKGROUND = "#f6f4f3"
    FONT = "#1b2021"
    SELECT_BUTTON = "#BAD87A"
    OCCUPIED_BUTTON = "#DE675F"
    LIST_BACKGROUND = "#D9D9D9"

class Config:
    API_BASE_URL = "http://127.0.0.1:8000/api"
    ROOMS_ENDPOINT = "/rooms/"
    REQUEST_TIMEOUT = 10

class RoomData:
    def __init__(self, id: int, raum_nr: str, is_occupied: bool):
        self.id = id
        self.raum_nr = raum_nr
        self.is_occupied = is_occupied

class Choose_RoomWindow(Gtk.Box):
    def __init__(self, parent_window: Gtk.Window) -> None:
        # Initialize GTK.Box
        super().__init__(homogeneous=False, spacing=20)
        self.set_orientation(Gtk.Orientation.VERTICAL)

        print("Initializing Choose_RoomWindow")
        self.parent_window = parent_window
        self._state = RoomState.IDLE
        self._rooms = []

        # Initialize logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self._init_ui()
        self._apply_styles()

        # Make sure everything is visible
        self.show_all()
        self.logger.info("Choose_RoomWindow initialization complete")

    def _init_ui(self) -> None:
        """Initialize the UI components"""
        self.logger.info("Starting UI initialization")

        # Container margins
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        # Header box
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        header_box.set_margin_bottom(20)

        # Title
        title = Gtk.Label(label="Hallo.")
        title.set_name("big_heading")
        title.set_halign(Gtk.Align.START)
        header_box.pack_start(title, True, True, 0)

        # Help button
        help_button = Gtk.Button(label="Hilfe")
        help_button.set_name("help_button")
        help_button.connect("clicked", self._show_help_dialog)
        header_box.pack_end(help_button, False, False, 0)

        self.pack_start(header_box, False, True, 0)
        self.logger.info("Header added")

        # Subtitle
        subtitle = Gtk.Label(label="Bitte ordne dem Gerät einen Raum zu:")
        subtitle.set_name("big_subheading")
        subtitle.set_halign(Gtk.Align.START)
        subtitle.set_margin_bottom(20)
        self.pack_start(subtitle, False, True, 0)
        self.logger.info("Subtitle added")

        # Room list container
        list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        list_box.set_margin_start(10)
        list_box.set_margin_end(10)

        # Add some test rooms for visibility testing
        for i in range(3):
            room_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            room_box.set_name("room_container")

            label = Gtk.Label(label=f"Raum {i+1}.0")
            label.set_name("room_label")
            label.set_halign(Gtk.Align.START)
            room_box.pack_start(label, True, True, 10)

            button = Gtk.Button(label="Auswählen")
            button.set_name("select_button")
            button.connect("clicked", self._on_room_selected, i + 1)  # Pass room ID
            room_box.pack_end(button, False, False, 10)

            list_box.pack_start(room_box, False, True, 0)
            self.logger.info(f"Added test room {i+1}")

        # Scrolled Window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)  # Ensures the scrolled window takes all available vertical space
        scrolled.set_hexpand(True)  # Ensures the scrolled window takes all available horizontal space
        scrolled.add(list_box)
        self.pack_start(scrolled, True, True, 0)

        # Store reference for later updates
        self.room_list = list_box
        self.logger.info("Room list container added")

    def _on_room_selected(self, button: Gtk.Button, room_id: int) -> None:
        """Handle room selection and forward to create_activity view"""
        self.logger.info(f"Room {room_id} selected")
        if hasattr(self.parent_window, "switch_to_create_activity"):
            self.parent_window.switch_to_create_activity(room_id)
        else:
            self.logger.error("Parent window does not support switching views")

    def _apply_styles(self) -> None:
        """Apply CSS styles"""
        css_provider = Gtk.CssProvider()
        css = f"""
            box {{
                background-color: {Colors.BACKGROUND};
            }}
            
            #big_heading {{
                font-size: 48px;
                font-weight: bold;
                color: {Colors.FONT};
            }}
            
            #big_subheading {{
                font-size: 24px;
                color: {Colors.FONT};
            }}
            
            #room_container {{
                background-color: {Colors.LIST_BACKGROUND};
                border-radius: 15px;
                padding: 10px;
                margin: 5px 0;
            }}
            
            #room_label {{
                font-size: 24px;
                color: {Colors.FONT};
            }}
            
            #select_button {{
                background-color: {Colors.SELECT_BUTTON};
                color: {Colors.FONT};
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }}
            
            #help_button {{
                background-color: white;
                color: {Colors.FONT};
                border: 2px solid {Colors.FONT};
                border-radius: 45px;
                padding: 5px 15px;
            }}
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.logger.info("Styles applied")

    def _show_help_dialog(self, button: Gtk.Button) -> None:
        """Show help dialog"""
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Was muss ich in diesem Anzeigefenster beachten?"
        )
        dialog.format_secondary_text(
            "In dieser Ansicht können Sie dem Gerät einen verfügbaren Raum zuweisen, "
            "um eine Aktivität zu erstellen. Verfügbare Räume erkennen Sie an der "
            "grünen Schaltfläche \"Auswählen\"."
        )
        dialog.run()
        dialog.destroy()
