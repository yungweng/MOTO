import gi
from typing import List, Optional, Dict
from enum import Enum
import requests
import logging
from datetime import datetime

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

class RoomState(Enum):
    IDLE = "idle"
    LOADING = "loading"
    ERROR = "error"

class Colors:
    BACKGROUND = "#f6f4f3"
    FONT = "#1b2021"
    HELP_BUTTON = "#ffffff"
    LIST_BACKGROUND = "#D9D9D9"
    GREEN = "#83cd2d"
    RED = "#ff3130"

class Config:
    API_BASE_URL = "https://127.0.0.1:8000/api"  # Note the https
    ROOMS_ENDPOINT = "/get_room_list/"
    VERIFY_SSL = False
    REQUEST_TIMEOUT = 10

class RoomData:
    def __init__(self, id: int, raum_nr: str, is_occupied: bool, color: str):
        self.id = id
        self.raum_nr = raum_nr
        self.is_occupied = is_occupied
        self.color = color

class Choose_RoomWindow(Gtk.Box):
    def __init__(self, parent_window: Gtk.Window) -> None:
        super().__init__(homogeneous=False, spacing=20)
        self.set_orientation(Gtk.Orientation.VERTICAL)

        self.parent_window = parent_window
        self._state = RoomState.IDLE
        self._rooms = []

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self._init_ui()
        self._apply_styles()

        # Set up room refresh
        GLib.timeout_add_seconds(30, self._refresh_rooms)
        GLib.idle_add(self._load_rooms)

        self.show_all()
        self.logger.info("Choose_RoomWindow initialization complete")

    def _init_ui(self) -> None:
        self.logger.info("Starting UI initialization")

        # TODO: Gebäude hinzufügen

        self.set_margin_top(30)
        self.set_margin_bottom(0)
        self.set_margin_start(20)
        self.set_margin_end(20)

        # Header
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        header_box.set_margin_bottom(20)

        logout_button = Gtk.Button(label="Abmelden")
        logout_button.set_name("help_button")
        logout_button.set_halign(Gtk.Align.START)
        header_box.pack_start(logout_button, False, False, 0)

        help_button = Gtk.Button(label="HILFE")
        help_button.set_name("help_button")
        help_button.connect("clicked", self._show_help_dialog)
        header_box.pack_end(help_button, False, False, 0)

        refresh_button = Gtk.Button(label="Aktualisieren")
        refresh_button.set_name("help_button")
        refresh_button.connect("clicked", lambda _: self._load_rooms())
        header_box.pack_end(refresh_button, False, False, 0)

        self.pack_start(header_box, False, True, 0)

        # Header title
        title = Gtk.Label(label="Hallo VORNAME")
        title.set_name("big_heading")
        title.set_halign(Gtk.Align.START)
        self.pack_start(title, False, True, 0)

        # Subtitle
        subtitle = Gtk.Label(label="Bitte ordne dem Gerät einen Raum zu:")
        subtitle.set_name("big_subheading")
        subtitle.set_halign(Gtk.Align.START)
        subtitle.set_margin_bottom(20)
        self.pack_start(subtitle, False, True, 0)

        # Room list
        self.room_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.room_list.set_margin_start(10)
        self.room_list.set_margin_end(0)
        self.room_list.set_name("room_list")

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_name("room_scrolled_window")
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        scrolled.add(self.room_list)
        self.pack_start(scrolled, True, True, 0)

        # Status bar
        self.status_bar = Gtk.Label(label="Zuletzt aktualisiert: 28.12.2024 12:00")
        self.status_bar.set_name("status_bar")
        self.status_bar.set_margin_bottom(10)
        self.pack_end(self.status_bar, False, True, 0)

    def _load_rooms(self) -> None:
        self._state = RoomState.LOADING
        try:
            headers = {
                "Authorization": f"Bearer {self.parent_window.access_token}",
                "Content-Type": "application/json"
            }

            response = requests.get(
                f"{Config.API_BASE_URL}{Config.ROOMS_ENDPOINT}",
                headers=headers,
                timeout=Config.REQUEST_TIMEOUT,
                verify=Config.VERIFY_SSL 
            )

            if response.status_code == 200:
                data = response.json()
                self._rooms_by_category = [] 

                for category_data in data:
                    category = category_data['kategorie']
                    rooms = [
                        RoomData(
                            id=room['id'],
                            raum_nr=room['raum_nr'],
                            is_occupied=room.get('belegt', False),
                            color=room['color'] 
                        )
                        for room in category_data['raeume']
                    ]
                    self._rooms_by_category.append({"kategorie": category, "raeume": rooms})

                self._update_room_list()
                self._state = RoomState.IDLE
            else:
                self.logger.error(f"API error: {response.status_code}")
                self._state = RoomState.ERROR

        except Exception as e:
            self.logger.error(f"Failed to load rooms: {e}")
            self._state = RoomState.ERROR


    def _update_room_list(self) -> None:
        for child in self.room_list.get_children():
            self.room_list.remove(child)

        for category_data in self._rooms_by_category:
            category = category_data['kategorie']
            rooms = category_data['raeume']

            category_label = Gtk.Label(label=f"Kategorie: {category}")
            category_label.set_name("category_label")
            category_label.set_halign(Gtk.Align.START)
            self.room_list.pack_start(category_label, False, True, 10)

            for room in sorted(rooms, key=lambda x: x.raum_nr):
                room_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
                room_box.set_name("room_container")

                label = Gtk.Label(label=f"Raum {room.raum_nr}")
                label.set_name("room_label")
                label.set_halign(Gtk.Align.START)
                room_box.pack_start(label, True, True, 10)

                button = Gtk.Button(label="Belegt" if room.is_occupied else "Auswählen")
                button.set_name("occupied_button" if room.is_occupied else "select_button")
                if not room.is_occupied:
                    button.connect("clicked", self._on_room_selected, room.id)
                button.set_sensitive(not room.is_occupied)
                room_box.pack_end(button, False, False, 10)

                self.room_list.pack_start(room_box, False, True, 0)

        self.room_list.show_all()


    def _refresh_rooms(self) -> bool:
        self._load_rooms()
        return True

    def _on_room_selected(self, button: Gtk.Button, room_id: int) -> None:
        self.logger.info(f"Room {room_id} selected")
        if hasattr(self.parent_window, "switch_to_create_activity"):
            self.parent_window.switch_to_create_activity(room_id)
        else:
            self.logger.error("Parent window does not support switching views")

    def _apply_styles(self) -> None:
        css_provider = Gtk.CssProvider()
        css = f"""
            box {{
                background: {Colors.BACKGROUND};
            }}
            
            #big_heading {{
                font-family: "Inter", sans-serif;
                font-size: 48px;
                font-weight: bold;
                color: {Colors.FONT};
            }}
            
            #big_subheading {{
                font-family: "Inter", sans-serif;
                font-size: 24px;
                color: {Colors.FONT};
            }}
            
            #category_label {{
                font-family: "Inter", sans-serif;
                font-size: 20px;
                color: {Colors.FONT};
                border-bottom: 2px solid {Colors.FONT};
            }}
            
            #room_container {{
                font-family: "Inter", sans-serif;
                background: {Colors.LIST_BACKGROUND};
                padding: 18px;
                margin: 5px 0;
                border-radius: 18px;
                box-shadow: rgba(0, 0, 0, 0.18) 0px 2px 4px;
                
            }}
            
            #room_label {{
                font-family: "Inter", sans-serif;
                font-size: 26px;
                color: {Colors.FONT};
                
            }}
                
            #room_list{{
                background: inherit;
                border-radius: 40px;
            }}
            
        
            #select_button {{
                font-family: "Inter", sans-serif;
                font-size: 20px;
                background: {Colors.GREEN};
                color: {Colors.FONT};
                border: none;
                border-radius: 10px;
                padding: 15px 25px;
                box-shadow: rgba(0, 0, 0, 0.18) 0px 2px 4px;
            }}
            
            #occupied_button {{
                font-family: "Inter", sans-serif;
                background: {Colors.RED};
                color: {Colors.FONT};
                border: none;
                border-radius: 10px;
                padding: 8px 16px;
                box-shadow: rgba(0, 0, 0, 0.18) 0px 2px 4px;
            }}
            
            #help_button {{
                font-family: "Inter", sans-serif;
                background: {Colors.HELP_BUTTON};
                color: {Colors.FONT};
                border: 2px solid {Colors.FONT};
                border-radius: 45px;
                padding: 5px 15px;
                font-size: 20px;
                box-shadow: rgba(0, 0, 0, 0.18) 0px 2px 4px;
            }}
            
            
        
            
            #status_bar {{
                font-family: "Inter", sans-serif;
                font-size: 12px;
                color: #666666;
            }}
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _show_help_dialog(self, button: Gtk.Button) -> None:
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