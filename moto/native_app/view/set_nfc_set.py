import gi
from typing import Optional, List
import logging

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class Colors:
    BACKGROUND = "#f6f4f3"
    FONT = "#1b2021"
    BLUE = "#4a90e2"
    GREEN = "#BAD87A"
    ORANGE = "#FFB043"
    INPUT_BG = "rgba(217, 217, 217, 0.5)"
    LIST_BG = "#D9D9D9"
    HELP_BUTTON = "#ffffff"

class SetNFCSetWindow(Gtk.Box):
    def __init__(self, parent_window: Gtk.Window, tag_id: str) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.parent_window = parent_window
        self.tag_id = tag_id

        self._init_ui()
        self._apply_styles()
        self.show_all()

    def _init_ui(self) -> None:
        self.set_margin_top(30)
        self.set_margin_bottom(30)
        self.set_margin_start(50)
        self.set_margin_end(50)

        # Header
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        back_button = Gtk.Button(label="← Zurück")
        back_button.set_name("help_button")
        back_button.connect("clicked", lambda x: self.parent_window.switch_page("set_nfc_scan"))
        header_box.pack_start(back_button, False, False, 0)

        help_button = Gtk.Button(label="HILFE")
        help_button.set_name("help_button")
        help_button.connect("clicked", self._show_help_dialog)
        header_box.pack_end(help_button, False, False, 0)

        self.pack_start(header_box, False, False, 0)

        # Title
        title = Gtk.Label()
        title.set_markup(f"<span size='24000'>Chip erkannt: [{self.tag_id}]</span>")
        title.set_name("heading")
        title.set_halign(Gtk.Align.START)
        self.pack_start(title, False, False, 0)

        subtitle = Gtk.Label(label="Weisen Sie das Armband bei Bedarf neu zu.")
        subtitle.set_name("subheading")
        subtitle.set_halign(Gtk.Align.START)
        self.pack_start(subtitle, False, False, 0)

        # Current assignment
        current_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        current_label = Gtk.Label(label="Aktuell Zugewiesen:")
        current_label.set_name("text_current")
        current_box.pack_start(current_label, False, False, 0)

        current_value = Gtk.Label(label="Niemand")
        current_value.set_name("current_value")
        current_box.pack_start(current_value, False, False, 0)

        self.pack_start(current_box, False, False, 20)

        # Search section
        search_label = Gtk.Label(label="Neu zuweisen:")
        search_label.set_name("text_new")
        search_label.set_halign(Gtk.Align.START)
        self.pack_start(search_label, False, False, 0)

        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        search_entry = Gtk.Entry()
        search_entry.set_placeholder_text("Namen eingeben..")
        search_entry.set_name("searchbar")
        search_box.pack_start(search_entry, True, True, 0)

        search_button = Gtk.Button(label="Suchen")
        search_button.set_name("search_button")
        search_box.pack_end(search_button, False, False, 0)

        self.pack_start(search_box, False, False, 0)

        # Results container with scrolling
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(300)

        self.results_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        scrolled.add(self.results_box)
        self.pack_start(scrolled, True, True, 0)

        # Add some test results
        self._add_result("Max Mustermann", "1", True)
        self._add_result("Erika Musterfrau", "2", False)

    def _add_result(self, name: str, user_id: str, is_staff: bool = False):
        result_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        result_box.set_name("pupil_container")

        name_label = Gtk.Label(label=name)
        name_label.set_name("text_pupil")
        result_box.pack_start(name_label, True, True, 30)

        assign_button = Gtk.Button(label="Zuweisen")
        assign_button.set_name("assign_button_orange" if is_staff else "assign_button")
        assign_button.connect("clicked", self._on_assign, user_id)
        result_box.pack_end(assign_button, False, False, 25)

        self.results_box.pack_start(result_box, False, False, 0)

    def _on_assign(self, button: Gtk.Button, user_id: str):
        # TODO: Implement API call to assign tag
        self.parent_window.switch_page("set_nfc_scan")

    def _show_help_dialog(self, button: Gtk.Button) -> None:
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Was muss ich in diesem Anzeigefenster beachten?"
        )
        dialog.format_secondary_text(
            "In dieser Ansicht können Sie ein NFC-Armband einem neuen Kind oder "
            "Betreuer zuweisen. Tippen Sie beim gewünschten Kind/Betreuer auf "
            "\"Zuweisen\", um das Armband zuzuordnen."
        )
        dialog.run()
        dialog.destroy()

    def _apply_styles(self) -> None:
        css_provider = Gtk.CssProvider()
        css = f"""
            #heading {{
                font-family: "Inter", sans-serif;
                font-size: 48px;
                font-weight: bold;
                color: {Colors.FONT};
            }}
            
            #subheading {{
                font-family: "Inter", sans-serif;
                font-size: 24px;
                color: {Colors.FONT};
            }}
            
            #help_button {{
                background: {Colors.HELP_BUTTON};
                color: {Colors.FONT};
                border: 2px solid {Colors.FONT};
                border-radius: 45px;
                padding: 10px 25px;
                font-size: 20px;
            }}
            
            #text_current {{
                font-family: "Inter", sans-serif;
                font-size: 26px;
                color: {Colors.FONT};
            }}
            
            #current_value {{
                background-color: {Colors.INPUT_BG};
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 26px;
                color: {Colors.FONT};
            }}
            
            #text_new {{
                font-family: "Inter", sans-serif;
                font-size: 30px;
                font-weight: 600;
                text-decoration: underline;
                color: {Colors.FONT};
            }}
            
            #searchbar {{
                background-color: {Colors.INPUT_BG};
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 24px;
                min-height: 50px;
            }}
            
            #search_button {{
                background-color: {Colors.BLUE};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 24px;
                min-width: 150px;
                font-weight: 600;
            }}
            
            #pupil_container {{
                background-color: {Colors.LIST_BG};
                border-radius: 18px;
                min-height: 80px;
                box-shadow: rgba(17, 17, 26, 0.1) 0px 4px 16px;
            }}
            
            #text_pupil {{
                font-family: "Inter", sans-serif;
                font-size: 27px;
                font-weight: 500;
                color: {Colors.FONT};
            }}
            
            #assign_button {{
                background-color: {Colors.GREEN};
                color: {Colors.FONT};
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 24px;
                font-weight: 500;
                min-width: 200px;
            }}
            
            #assign_button_orange {{
                background-color: {Colors.ORANGE};
                color: {Colors.FONT};
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 24px;
                font-weight: 500;
                min-width: 200px;
            }}
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )