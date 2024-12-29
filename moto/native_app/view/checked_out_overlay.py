import gi
from typing import Optional, Callable
import logging
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk

class Colors:
    BACKGROUND_OVERLAY = "rgba(255, 255, 255, 0.95)"
    FONT = "#1b2021"
    GREEN = "#84cc2d"

class CheckedOutOverlay(Gtk.Overlay):
    def __init__(self, parent_window: Gtk.Window, user_name: str, callback: Optional[Callable] = None) -> None:
        super().__init__()

        # Main content box
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content_box.set_name("overlay_box")

        # Size and position control
        content_box.set_halign(Gtk.Align.CENTER)
        content_box.set_valign(Gtk.Align.CENTER)
        content_box.set_margin_top(200)
        content_box.set_margin_bottom(200)
        content_box.set_margin_start(400)
        content_box.set_margin_end(400)

        # Goodbye message
        welcome_label = Gtk.Label()
        welcome_label.set_markup(f"<span size='12000'>Tschüss {user_name}!</span>")
        welcome_label.set_name("overlay_heading")
        content_box.pack_start(welcome_label, False, False, 5)

        # Image
        try:
            image = Gtk.Image.new_from_file("img/checked_out.png")
            image.set_pixel_size(60)
            content_box.pack_start(image, False, False, 5)
        except Exception as e:
            logging.error(f"Failed to load checked_out image: {e}")

        self.add(content_box)
        self._apply_styles()
        self.show_all()

        self.callback = callback
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