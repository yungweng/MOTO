import gi
from typing import Optional, Callable
import logging

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk

class Colors:
    BACKGROUND = "#f6f4f3"
    FONT = "#1b2021"
    GREEN = "#83cd2d"
    RED = "#ff3130"

class RemoveTabletOverlay(Gtk.Overlay):
    def __init__(self, parent_window: Gtk.Window, callback: Optional[Callable] = None) -> None:
        super().__init__()

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        main_box.set_valign(Gtk.Align.CENTER)

        # Title
        title = Gtk.Label()
        title.set_markup("<span size='36000'>Wollen Sie das Gerät wirklich abmelden?</span>")
        title.set_name("overlay_heading")
        title.set_margin_top(100)
        title.set_margin_bottom(160)
        main_box.pack_start(title, False, False, 0)

        # Buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        button_box.set_halign(Gtk.Align.CENTER)

        no_button = Gtk.Button(label="Nein")
        no_button.set_name("abort_button")
        no_button.connect("clicked", lambda w: self._on_no_clicked(parent_window))
        button_box.pack_start(no_button, False, False, 20)

        yes_button = Gtk.Button(label="Ja")
        yes_button.set_name("select_button")
        yes_button.connect("clicked", lambda w: self._on_yes_clicked(parent_window))
        button_box.pack_start(yes_button, False, False, 20)

        main_box.pack_start(button_box, True, False, 0)

        self.add(main_box)
        self._apply_styles()
        self.show_all()

    def _apply_styles(self) -> None:
        css_provider = Gtk.CssProvider()
        css = f"""
            #overlay_heading {{
                font-family: "Inter", sans-serif;
                font-weight: bold;
                color: {Colors.FONT};
            }}
            
            #select_button, #abort_button {{
                font-family: "Inter", sans-serif;
                font-size: 28px;
                font-weight: bold;
                border: none;
                border-radius: 18px;
                padding: 10px 40px;
                min-width: 260px;
                min-height: 100px;
                box-shadow: rgba(0, 0, 0, 0.36) 0px 6px 20px 2px;
            }}
            
            #select_button {{
                background: {Colors.GREEN};
                color: {Colors.FONT};
            }}
            
            #abort_button {{
                background: {Colors.RED};
                color: white;
            }}
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _on_yes_clicked(self, parent_window: Gtk.Window) -> None:
        parent_window.access_token = None
        parent_window.refresh_token = None
        parent_window.switch_page("choose_room")
        self.destroy()

    def _on_no_clicked(self, parent_window: Gtk.Window) -> None:
        parent_window.switch_page("master_tablet")
        self.destroy()