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
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        # Header with login button
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header_box.set_name("header_container_mid")

        login_button = Gtk.Button(label="Login")
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
        image = Gtk.Image()
        image.set_name("nfc_scan")
        # You might want to replace this with an actual NFC icon
        image.set_from_icon_name("nfc", Gtk.IconSize.DIALOG)
        image.set_pixel_size(200)  # Make the icon larger
        mid_container.pack_start(image, True, True, 20)

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
        self.pack_start(self.tag_id_entry, False, False, 0)

    def _apply_styles(self) -> None:
        css_provider = Gtk.CssProvider()
        css = f"""
            #header_container_mid {{
                margin: 20px;
            }}
            
            #login_button {{
                background: {Colors.HELP_BUTTON};
                color: {Colors.FONT};
                border: 3px solid {Colors.FONT};
                border-radius: 45px;
                padding: 10px 20px;
                font-size: 20px;
                min-width: 130px;
                min-height: 46px;
            }}
            
            #mid_container {{
                margin: 20px;
            }}
            
            #default_heading_mid {{
                font-weight: bold;
                font-size: 70px;
                margin: 20px 0;
            }}
            
            #nfc_scan {{
                margin: 20px;
                opacity: 0.8;
            }}
            
            #explanation {{
                font-size: 25px;
                margin: 10px 0;
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