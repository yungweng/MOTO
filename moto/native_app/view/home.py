import gi
from typing import Optional
import logging

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

class Colors:
    BACKGROUND = "#f6f4f3"
    FONT = "#1b2021"
    HELP_BUTTON = "#ffffff"

class HomeWindow(Gtk.Box):
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
        self.set_margin_bottom(10)
        self.set_margin_start(20)
        self.set_margin_end(20)

        # Header with login button
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header_box.set_name("header_container_mid")

        login_button = Gtk.Button(label="Einstellungen")
        login_button.set_name("login_button")
        login_button.connect("clicked", self._on_login_clicked)
        header_box.pack_end(login_button, False, False, 0)

        self.pack_start(header_box, False, False, 0)

        # Middle container
        mid_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        mid_container.set_name("mid_container")

        # Room number
        room_label = Gtk.Label()
        room_label.set_markup(f"<span size='50000'>Raum {self.room_id}</span>")
        room_label.set_name("default_heading_mid")
        mid_container.pack_start(room_label, False, True, 20)

        # NFC Image placeholder
        logo_image = Gtk.Image.new_from_file("img/nfc_pfeil.png")
        logo_image.set_margin_bottom(5)     # Add some spacing below the image
        mid_container.pack_start(logo_image, False, False, 10)


        # Explanation text
        explanation = Gtk.Label(
            label="Halte dein Armband an das Logo um dich an- oder abzumelden!"
        )
        explanation.set_name("explanation")
        mid_container.pack_start(explanation, False, True, 10)

        self.pack_start(mid_container, True, True, 0)

        # Hidden form for NFC tag ID
        self.tag_id_entry = Gtk.Entry()
        self.tag_id_entry.set_visible(False)
        self.tag_id_entry.set_no_show_all(True)
        self.pack_start(self.tag_id_entry, False, False, 0)

    def _apply_styles(self) -> None:
        css_provider = Gtk.CssProvider()
        css = f"""
            #header_container_mid {{
                font-family: "Inter", sans-serif;
                margin: 0px;
            }}
            
            #login_button {{
                font-family: "Inter", sans-serif;
                background: {Colors.HELP_BUTTON};
                color: {Colors.FONT};
                border: 2px solid {Colors.FONT};
                border-radius: 45px;
                padding: 5px 15px;
                font-size: 20px;
                box-shadow: rgba(0, 0, 0, 0.2) 15px 28px 25px -18px;
            }}
            #login_button:hover {{
                box-shadow: rgba(0, 0, 0, 0.3) 2px 8px 8px -5px;
            }}
            
            #mid_container {{
                margin: 0px;
            }}
            
            #default_heading_mid {{
                font-family: "Inter", sans-serif;
                font-weight: bold;
                font-size: 70px;
                color: {Colors.FONT};
                margin: 0px 0;
            }}
            

            
            #explanation {{
                font-family: "Inter", sans-serif;
                font-size: 25px;
                color: {Colors.FONT};
                margin: 0px 0;
            }}
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _on_login_clicked(self, button: Gtk.Button) -> None:
        """Handle login button click"""
        self.parent_window.switch_page("login_window")

    def _on_nfc_tag_detected(self, tag_id: str) -> None:
        """Handle NFC tag detection"""
        self.tag_id_entry.set_text(tag_id)
        # TODO: Add API call to handle check-in/check-out
        # Similar to the Django view logic