import gi
from typing import Optional
import logging

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class Colors:
    BACKGROUND = "#f6f4f3"
    FONT = "#1b2021"
    HELP_BUTTON = "#ffffff"
    BUTTON_BG = "rgba(185, 185, 185, 0.75)"

class MasterTabletWindow(Gtk.Box):
    def __init__(self, parent_window: Gtk.Window) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.parent_window = parent_window
        self._init_ui()
        self._apply_styles()
        self.show_all()

    def _init_ui(self) -> None:
        # Container margins
        self.set_margin_top(30)
        self.set_margin_bottom(30)
        self.set_margin_start(20)
        self.set_margin_end(20)

        # Header
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        back_button = Gtk.Button(label="← Zurück")
        back_button.set_name("help_button")
        back_button.connect("clicked", lambda x: self.parent_window.switch_page("home"))
        header_box.pack_start(back_button, False, False, 0)

        help_button = Gtk.Button(label="HILFE")
        help_button.set_name("help_button")
        help_button.connect("clicked", self._show_help_dialog)
        header_box.pack_end(help_button, False, False, 0)

        self.pack_start(header_box, False, False, 0)

        # Title and subtitle
        title = Gtk.Label(label="Einstellungen")
        title.set_name("heading_2")
        title.set_halign(Gtk.Align.START)
        self.pack_start(title, False, False, 0)

        subtitle = Gtk.Label(label="Wählen Sie eine der folgenden Aktionen aus:")
        subtitle.set_name("subheading_2")
        subtitle.set_halign(Gtk.Align.START)
        self.pack_start(subtitle, False, False, 0)

        # Buttons container
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        button_box.set_halign(Gtk.Align.CENTER)

        # Create buttons
        buttons = [
            ("Gerät abmelden", lambda x: self.parent_window.switch_page("remove_tablet")),
            ("Raumangaben ändern", lambda x: self.parent_window.switch_page("change_roomdata")),
            ("NFC Chip neu zuweisen", lambda x: self.parent_window.switch_page("set_nfc_scan"))
        ]

        for label, callback in buttons:
            button_container = self._create_action_button(label, callback)
            button_box.pack_start(button_container, False, True, 10)

        self.pack_start(button_box, True, True, 0)
        self._apply_styles()
        self.show_all()

    def _create_action_button(self, label: str, callback: callable) -> Gtk.Button:
        button = Gtk.Button(label=label)
        button.set_name("button_style1")
        button.connect("clicked", callback)
        return button

    def _apply_styles(self) -> None:
        css_provider = Gtk.CssProvider()
        css = f"""
            #heading_2 {{
                font-family: "Inter", sans-serif;
                font-size: 48px;
                font-weight: 600;
                color: {Colors.FONT};
            }}
            
            #subheading_2 {{
                font-family: "Inter", sans-serif;
                font-size: 32px;
                color: {Colors.FONT};
            }}
            
            #help_button {{
                background: {Colors.HELP_BUTTON};
                color: {Colors.FONT};
                border: 2px solid {Colors.FONT};
                border-radius: 45px;
                padding: 10px 25px;
                font-size: 20px;
                box-shadow: rgba(0, 0, 0, 0.2) 15px 28px 25px -18px;
            }}
            
            #button_style1 {{
                font-family: "Inter", sans-serif;
                background: {Colors.BUTTON_BG};
                border-radius: 24px;
                color: {Colors.FONT};
                font-size: 30px;
                font-weight: bold;
                min-height: 220px;
                min-width: 300px;
                box-shadow: rgba(0, 0, 0, 0.2) 15px 28px 25px -18px;
            }}
            
            #button_style1:hover {{
                box-shadow: rgba(0, 0, 0, 0.3) 2px 8px 8px -5px;
            }}
            #help_button:hover {{
                box-shadow: rgba(0, 0, 0, 0.3) 2px 8px 8px -5px;
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
            "In dieser Masteransicht können Sie zwischen verschiedenen Funktionen "
            "der App navigieren. Sie müssen auf die grauen Schaltflächen klicken, "
            "um in das nächste Fenster zu navigieren."
        )
        dialog.run()
        dialog.destroy()