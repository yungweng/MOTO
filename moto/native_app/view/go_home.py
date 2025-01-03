import gi
from typing import Optional, Callable
import logging

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

class Colors:
    BACKGROUND = "#f6f4f3"
    FONT = "#1b2021"
    GREEN = "#84cc2d"
    INPUT_BG = "rgba(217, 217, 217, 0.5)"
    VERY_WELL = "#83CD2D"
    OKAY = "#F78C10"
    BAD = "#FF3130"


class GoHomeWindow(Gtk.Box):
    def __init__(self, parent_window: Gtk.Window) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.parent_window = parent_window
        self.logger = logging.getLogger(__name__)

        self._init_ui()
        self._apply_styles()
        self.show_all()

        # Auto redirect after 3 seconds if no feedback given
        GLib.timeout_add(300000, self._on_timeout) # Für Debug erhöht. Debuggende Grüße, Flo

    def _init_ui(self) -> None:
        # Container margins
        self.set_margin_top(50)
        self.set_margin_bottom(50)
        self.set_margin_start(50)
        self.set_margin_end(50)

        # Title
        title = Gtk.Label(label="Auf Wiedersehen!") # TODO: @chris include name of user
        title.set_name("heading_type1")
        title.set_margin_bottom(0)
        self.pack_start(title, False, False, 0)

        # Feedback buttons container
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        button_box.set_halign(Gtk.Align.CENTER)

        # Bad button
        bad = Gtk.Image.new_from_file("img/negative_smiley1.png")
        bad.set_margin_bottom(0)  # Add some spacing below the image
        button_box.pack_start(bad, False, False, 0)

        # Neutral button
        neutral = Gtk.Image.new_from_file("img/neutral_smiley1.png")
        neutral.set_margin_bottom(0)  # Add some spacing below the image
        button_box.pack_start(neutral, False, False, 0)

        # Positive button
        positive = Gtk.Image.new_from_file("img/positive_smiley1.png")
        positive.set_margin_bottom(0)  # Add some spacing below the image
        button_box.pack_start(positive, False, False, 0)



        self.pack_start(button_box, True, True, 0)


        # Subtitle
        subtitle = Gtk.Label(label="Wie war dein Tag heute?")
        subtitle.set_name("subtitle")
        subtitle.set_margin_top(0)
        self.pack_start(subtitle, False, False, 0)

    def _create_feedback_button(self, image_path: str, label_text: str, button_id: str,
                                callback: Callable) -> Gtk.Box:
        # Container for image and label
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        container.set_name(button_id)

        # Create button with image
        try:
            image = Gtk.Image.new_from_file(image_path)
            image.set_pixel_size(80)
        except Exception as e:
            self.logger.error(f"Failed to load image {image_path}: {e}")
            image = Gtk.Image()

        button = Gtk.Button()
        button.set_image(image)
        button.set_name(f"{button_id}_button")
        button.connect("clicked", callback)
        container.pack_start(button, False, False, 0)

        # Label
        label = Gtk.Label(label=label_text)
        label.set_name("feedback_label")
        container.pack_start(label, False, False, 0)

        return container

    def _handle_feedback(self, feedback_type: str) -> None:
        """Handle feedback submission"""
        try:
            headers = {
                "Authorization": f"Bearer {self.parent_window.access_token}",
                "Content-Type": "application/json"
            }
            # TODO: Implement API call for feedback
            # After feedback is sent, redirect
            self.parent_window.switch_page("login")
        except Exception as e:
            self.logger.error(f"Error sending feedback: {e}")
            self.parent_window.switch_page("login")

    def _on_timeout(self) -> bool:
        """Handle automatic redirect after timeout"""
        self.parent_window.switch_page("login")
        return False

    def _apply_styles(self) -> None:
        css_provider = Gtk.CssProvider()
        css = f"""
            #heading_type1 {{
                font-family: "Inter", sans-serif;
                font-size: 56px;
                font-weight: bold;
                color: {Colors.FONT};
            }}
            
            #subtitle {{
                font-family: "Inter", sans-serif;
                font-weight: bold;
                font-size: 36px;
                color: {Colors.FONT};
            }}
            
            
            #feedback_label {{
                font-family: "Inter", sans-serif;
                font-size: 18px;
                color: {Colors.FONT};
            }}
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )