import gi
from typing import Optional
import logging

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

class Colors:
    BACKGROUND = "#f6f4f3"
    FONT = "#1b2021"
    BUTTON_BG = "#ffffff"

class SetNFCScanOverlay(Gtk.Box):
    def __init__(self, parent_window: Gtk.Window) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.parent_window = parent_window
        self._init_ui()
        self._apply_styles()
        self.show_all()

    def _init_ui(self) -> None:
        self.set_margin_top(50)
        self.set_margin_bottom(50)
        self.set_margin_start(50)
        self.set_margin_end(50)

        # Header with back and help buttons
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        back_button = Gtk.Button(label="← Zurück")
        back_button.set_name("back_button")
        back_button.connect("clicked", self._on_back_clicked)
        header_box.pack_start(back_button, False, False, 0)

        help_button = Gtk.Button(label="HILFE")
        help_button.set_name("help_button")
        help_button.connect("clicked", self._show_help_dialog)
        header_box.pack_end(help_button, False, False, 0)

        self.pack_start(header_box, False, False, 0)

        # Title
        self.title_label = Gtk.Label(
            label="Scannen Sie den NFC-Chip den Sie neu setzen möchten."
        )
        self.title_label.set_name("heading_type1")
        self.pack_start(self.title_label, False, False, 30)

        # NFC Image
        try:
            image = Gtk.Image.new_from_file("img/placeholder_nfc_scan_transparent.png")
            image.set_pixel_size(300)
            self.pack_start(image, True, True, 0)
        except Exception as e:
            logging.error(f"Failed to load NFC scan image: {e}")

    def _apply_styles(self) -> None:
        css_provider = Gtk.CssProvider()
        css = f"""
            #heading_type1 {{
                font-family: "Inter", sans-serif;
                font-size: 24px;
                font-weight: 600;
                color: {Colors.FONT};
            }}
            
            #back_button {{
                background: none;
                border: none;
                color: {Colors.FONT};
                font-family: "Inter", sans-serif;
                font-size: 20px;
                padding: 10px 20px;
            }}
            
            #help_button {{
                background: {Colors.BUTTON_BG};
                color: {Colors.FONT};
                border: 2px solid {Colors.FONT};
                border-radius: 45px;
                padding: 10px 25px;
                font-family: "Inter", sans-serif;
                font-size: 20px;
            }}
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _on_back_clicked(self, button: Gtk.Button) -> None:
        self.parent_window.switch_page("master_tablet")

    def _show_help_dialog(self, button: Gtk.Button) -> None:
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Was muss ich in diesem Anzeigefenster beachten?"
        )
        dialog.format_secondary_text(
            "Hier können Sie den NFC-Chip eines Kinds neu zuweisen. "
            "Halten Sie das Armband dafür an den Scanner. "
            "Nach erfolreicher Identifizierung des NFC-Chips öffnet "
            "sich ein Fenster, in dem Sie den Chip neu zuweisen können."
        )
        dialog.run()
        dialog.destroy()