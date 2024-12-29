import gi
from typing import Optional, Callable
import logging
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk

class Colors:
    BACKGROUND_OVERLAY = "rgba(255, 255, 255, 0.95)"
    FONT = "#1b2021"
    GREEN = "#84cc2d"

class CheckedInOverlay(Gtk.Overlay):
    def __init__(self, parent_window: Gtk.Window, user_name: str, callback: Optional[Callable] = None) -> None:
        super().__init__()

        self.parent_window = parent_window
        self.callback = callback
        self.logger = logging.getLogger(__name__)

        # Main center box
        self.overlay_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.overlay_box.set_name("overlay_box")
        self.overlay_box.set_size_request(100, 100)


        # Size and position control
        center_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        center_box.set_valign(Gtk.Align.CENTER)
        center_box.set_halign(Gtk.Align.CENTER)

        # Welcome message
        welcome_label = Gtk.Label()
        welcome_label.set_markup(f"<span size='12000'>Hallo {user_name}!</span>")
        welcome_label.set_name("overlay_heading")
        center_box.pack_start(welcome_label, False, False, 10)

        # Image
        try:
            image = Gtk.Image.new_from_file("img/checked_in.png")
            image.set_pixel_size(60)
            center_box.pack_start(image, False, False, 20)
        except Exception as e:
            logging.error(f"Failed to load checked_in image: {e}")

        self.add(center_box)
        self._apply_styles()
        self.show_all()

        self.callback = callback
        # Hier Zeit bis es weg geht, kann für Debugging länger gemacht werden. Debuggende LG
        GLib.timeout_add(1000, self._on_timeout)

    def _apply_styles(self) -> None:
        css_provider = Gtk.CssProvider()
        css = f"""
            #overlay_box {{
                background-color: {Colors.BACKGROUND_OVERLAY};
                border-radius: 10px;
                padding: 15px;
            }}
            
            #overlay_heading {{
                font-family: "Inter", sans-serif;
                font-weight: bold;
                color: {Colors.FONT};
            }}
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _on_timeout(self) -> bool:
        if self.callback:
            self.callback()
        self.destroy()
        return False