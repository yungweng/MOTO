import gi
from typing import Optional, Callable
import logging
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk

class Colors:
    BACKGROUND_OVERLAY = "#f6f4f3"
    FONT = "#1b2021"
    DOOR = "#F78C10"
    TOILET = "#5080d8"
    SCHOOLYARD = "#83cd2d"
    HOME = "#ff3130"

class LeaveRoomOverlay(Gtk.Overlay):
    def __init__(self, parent_window: Gtk.Window, user_name: str, callback: Optional[Callable] = None) -> None:
        super().__init__()

        self.parent_window = parent_window
        self.callback = callback
        self.logger = logging.getLogger(__name__)

        # Main vertical box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        main_box.set_margin_top(90)
        main_box.set_margin_left(50)
        main_box.set_margin_right(50)

        # Title
        title = Gtk.Label()
        title.set_markup(f"<span size='50000'>Tschüss {user_name}!</span>")
        title.set_name("overlay_heading")
        main_box.pack_start(title, False, False, 0)

        # Subtitle
        subtitle = Gtk.Label()
        subtitle.set_markup("<span size='25000'>Wohin möchtest du gehen?</span>")
        subtitle.set_name("overlay_subheading")
        main_box.pack_start(subtitle, False, False, 20)

        # Buttons container
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        button_box.set_halign(Gtk.Align.CENTER)

        # Create buttons
        buttons = [
            ("Raum wechseln", "leave_room_icon.png", Colors.DOOR, self._on_change_room),
            ("Toilette", "toilet_icon.png", Colors.TOILET, self._on_toilet),
            ("Schulhof", "school_yard_icon.png", Colors.SCHOOLYARD, self._on_schoolyard),
            ("Nach Hause", "home.png", Colors.HOME, self._on_go_home)
        ]

        for label, icon, color, callback in buttons:
            button_container = self._create_button(label, icon, color, callback)
            button_box.pack_start(button_container, False, True, 10)

        main_box.pack_start(button_box, True, True, 0)
        self.add(main_box)
        self._apply_styles()
        self.show_all()

        # Auto timeout after 5 seconds
        GLib.timeout_add(500000, lambda: self._on_change_room()) # increased for debugging

    def _create_button(self, label: str, icon_name: str, color: str, callback: Callable) -> Gtk.Box:
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        container.set_name("button_container")

        button = Gtk.Button()
        button.set_name(f"custom_button_{color[1:]}")  # Remove # from color

        try:
            image = Gtk.Image.new_from_file(f"img/{icon_name}")
            image.set_pixel_size(80)
            button.set_image(image)
        except Exception as e:
            self.logger.error(f"Failed to load image {icon_name}: {e}")

        button.connect("clicked", lambda w: callback())
        container.pack_start(button, False, False, 0)

        label_widget = Gtk.Label(label=label)
        label_widget.set_name("button_label")
        container.pack_start(label_widget, False, False, 0)

        return container

    def _apply_styles(self) -> None:
        css_provider = Gtk.CssProvider()
        css = f"""
            #overlay_heading, #overlay_subheading {{
                font-family: "Inter", sans-serif;
                font-weight: bold;
                color: {Colors.FONT};
            }}

            #button_container {{
                background: none;
                padding: 10px;
            }}

            #button_label {{
                font-family: "Inter", sans-serif;
                font-size: 26px;
                font-weight: 600;
                color: {Colors.FONT};
            }}

            #custom_button_{Colors.DOOR[1:]} {{
                background: {Colors.DOOR};
                border: none;
                border-radius: 18px;
                min-width: 300px;
                min-height: 300px;
                box-shadow: rgba(0, 0, 0, 0.36) 0px 6px 20px 2px;
            }}

            #custom_button_{Colors.TOILET[1:]} {{
                background: {Colors.TOILET};
                border: none;
                border-radius: 18px;
                min-width: 300px;
                min-height: 300px;
                box-shadow: rgba(0, 0, 0, 0.36) 0px 6px 20px 2px;
            }}

            #custom_button_{Colors.SCHOOLYARD[1:]} {{
                background: {Colors.SCHOOLYARD};
                border: none;
                border-radius: 18px;
                min-width: 300px;
                min-height: 300px;
                box-shadow: rgba(0, 0, 0, 0.36) 0px 6px 20px 2px;
            }}

            #custom_button_{Colors.HOME[1:]} {{
                background: {Colors.HOME};
                border: none;
                border-radius: 18px;
                min-width: 300px;
                min-height: 300px;
                box-shadow: rgba(0, 0, 0, 0.36) 0px 6px 20px 2px;
            }}
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _on_change_room(self) -> None:
        self.parent_window.show_checked_out_overlay("User", lambda: self.parent_window.switch_page("choose_room"))
        self.destroy()
        return False

    def _on_toilet(self) -> None:
        self.parent_window.show_checked_out_overlay("User", lambda: self.parent_window.switch_page("home"))
        self.destroy()

    def _on_schoolyard(self) -> None:
        self.parent_window.show_checked_out_overlay("User", lambda: self.parent_window.switch_page("home"))
        self.destroy()

    def _on_go_home(self) -> None:
        self.parent_window.switch_page("go_home")
        self.destroy()