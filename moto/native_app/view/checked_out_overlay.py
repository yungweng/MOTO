import gi
from typing import Optional, Callable
import logging
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk

class Colors:
    BACKGROUND_OVERLAY = "rgba(255, 255, 255, 0.95)"
    FONT = "#1b2021"
    GREEN = "#83cd2d"

class CheckedOutOverlay(Gtk.Overlay):
    def __init__(self, parent_window: Gtk.Window, user_name: str, callback: Optional[Callable] = None) -> None:
        super().__init__()

        self.parent_window = parent_window
        self.callback = callback
        self.logger = logging.getLogger(__name__)

        # Size and position control
        center_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)


        # Welcome message
        welcome_label = Gtk.Label()
        welcome_label.set_markup(f"<span size='50000'>Tschüss {user_name}!</span>")
        welcome_label.set_margin_top(100)
        welcome_label.set_name("overlay_heading")
        center_box.pack_start(welcome_label, False, True, 20)

        # Image
        try:
            image = Gtk.Image.new_from_file("img/checked_out.png")
            image.set_pixel_size(60)
            image.set_margin_start(50)
            center_box.pack_start(image, False, False, 10)
        except Exception as e:
            logging.error(f"Failed to load checked_in image: {e}")

        self.add(center_box)
        self._apply_styles()
        self.show_all()

        self.callback = callback
        # Hier Zeit bis es weg geht, kann für Debugging länger gemacht werden. Debuggende LG
        GLib.timeout_add(10000, self._on_timeout)

    def _apply_styles(self) -> None:
        css_provider = Gtk.CssProvider()
        css = f"""
            
            
            #overlay_heading {{
                font-family: "Inter", sans-serif;
                font-weight: bold;
                font-size: 70px;
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