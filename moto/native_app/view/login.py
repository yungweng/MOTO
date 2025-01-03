import gi
from typing import Optional
from enum import Enum
import requests
import logging
from urllib3.exceptions import InsecureRequestWarning
import urllib3
# Suppress only the single warning from urllib3 needed.
urllib3.disable_warnings(InsecureRequestWarning)

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

class LoginState(Enum):
    """States for the login process"""
    IDLE = "idle"
    LOADING = "loading"
    ERROR = "error"
    SUCCESS = "success"

class Colors:
    """Color constants from CSS"""
    BACKGROUND = "#f6f4f3"
    FONT = "#1b2021"
    ERROR = "#de675f"
    HELP_BUTTON = "#ffffff"
    INPUT_BG = "rgba(217, 217, 217, 0.5)"
    GREEN = "#84cc2d"

class Config:
    """Configuration settings"""
    API_BASE_URL = "https://127.0.0.1:8000/api"
    LOGIN_ENDPOINT = "/login/"
    GET_USER_ENDPOINT = "/get_user_by_id/"
    VERIFY_SSL = False  # For development only
    REQUEST_TIMEOUT = 10  # seconds

class LoginWindow(Gtk.Box):
    """Login window component matching web styling and functionality"""

    def __init__(self, parent_window: Gtk.Window) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.parent_window = parent_window
        self._state = LoginState.IDLE
        self._setup_logging()
        self._init_ui()
        self._apply_styles()

    def _setup_logging(self) -> None:
        """Initialize logging configuration"""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def _init_ui(self) -> None:
        """Initialize the UI components with webapp styling"""
        # Main container styling
        self.set_margin_top(50)
        self.set_margin_bottom(50)
        self.set_margin_start(50)
        self.set_margin_end(50)

        # Header with help button
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header.set_margin_bottom(20)

        help_button = self._create_help_button()
        header.pack_end(help_button, False, False, 20)
        self.pack_start(header, False, False, 0)

        # MOTO Logo above title
        logo_image = Gtk.Image.new_from_file("img/moto_transparent_200.png")
        logo_image.set_margin_bottom(5)  # Add some spacing below the image
        self.pack_start(logo_image, False, False, 0)

        # Title
        title = Gtk.Label(label="Login")
        title.set_name("heading_type1")
        title.set_margin_bottom(20)

        self.pack_start(title, False, False, 0)

        # Login form
        form_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        form_box.set_margin_start(200)
        form_box.set_margin_end(200)

        # Username field
        self.username_entry = self._create_entry("Benutzername")
        form_box.pack_start(self.username_entry, False, False, 0)
        self.username_entry.connect("activate", lambda w: self.password_entry.grab_focus())

        # Password field
        self.password_entry = self._create_entry("Passwort", True)
        form_box.pack_start(self.password_entry, False, False, 0)
        self.password_entry.connect("activate", lambda w: self.invisible_submit.clicked())

        self.pack_start(form_box, False, False, 0)

        # Create an invisible button that will be activated by Enter key
        self.invisible_submit = Gtk.Button()
        self.invisible_submit.connect("clicked", self._handle_login)
        self.invisible_submit.set_can_focus(False)

        # Login button
        button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        button_box.set_margin_start(450)
        button_box.set_margin_end(450)
        button_box.set_margin_top(20)
        self.login_button = Gtk.Button(label="Anmelden")
        self.login_button.set_name("login_button")
        self.login_button.set_size_request(100, 50)
        self.login_button.connect("clicked", self._handle_login)
        button_box.pack_start(self.login_button, False, False, 0)

        self.pack_start(button_box, False, False, 0)

        # Forgot password
        self.password_label = Gtk.Label(label="Passwort vergessen?")
        self.password_label.set_name("password_label")
        self.password_label.set_margin_top(0)
        self.pack_start(self.password_label, False, False, 0)

        # Error message area
        self.error_label = Gtk.Label()
        self.error_label.set_name("error_label")
        self.error_label.set_margin_top(0)
        self.pack_start(self.error_label, False, False, 0)

    def _create_help_button(self) -> Gtk.Button:
        """Create help button matching web styling"""
        button = Gtk.Button(label="HILFE")
        button.set_name("help_button")
        button.connect("clicked", self._show_help_dialog)
        return button

    def _create_entry(self, placeholder: str, is_password: bool = False) -> Gtk.Entry:
        """Create styled entry field matching web styling"""
        entry = Gtk.Entry()
        entry.set_placeholder_text(placeholder)
        if is_password:
            entry.set_visibility(False)
        entry.set_name("login_entry")
        return entry



    def _apply_styles(self) -> None:
        """Apply CSS styles to match web version"""
        css_provider = Gtk.CssProvider()
        css = f"""
            #heading_type1 {{
                font-family: "Inter", sans-serif;
                font-size: 50px;
                font-weight: bold;
                color: {Colors.FONT};
            }}
            
            #login_entry {{
                font-family: "Inter", sans-serif;
                font-size: 24px;
                padding: 8px;
                border-radius: 10px;
                background: {Colors.INPUT_BG};
                color: {Colors.FONT};
                margin: 5px 0;
            }}
            
            #login_button {{
                font-family: "Inter", sans-serif;
                background: {Colors.GREEN};
                color: {Colors.FONT};
                font-size: 26px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 10px;
                box-shadow: rgba(0, 0, 0, 0.18) 0px 2px 4px;
            }}
            
            #help_button {{
                font-family: "Inter", sans-serif;
                background: {Colors.HELP_BUTTON};
                color: {Colors.FONT};
                border: 2px solid {Colors.FONT};
                border-radius: 45px;
                padding: 10px 25px;
                font-size: 20px;
                box-shadow: rgba(0, 0, 0, 0.18) 0px 2px 4px;
            }}
            
            #password_label {{
                font-family: "Inter", sans-serif;
                font-size: 14px;
                color: {Colors.FONT};
                font-style: italic;
                text-decoration: underline;
            
            }}
            
            #error_label {{
                font-family: "Inter", sans-serif;
                color: {Colors.ERROR};
                font-size: 18px;
                font-weight: 500;
            }}
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _handle_login(self, button: Gtk.Button) -> None:
        """Handle login button click"""
        if self._state == LoginState.LOADING:
            return

        username = self.username_entry.get_text()
        password = self.password_entry.get_text()

        if not username or not password:
            self._show_error("Benutzername oder Passwort ist falsch")
            return

        self._set_loading_state(True)

        try:
            response = requests.post(
                f"{Config.API_BASE_URL}{Config.LOGIN_ENDPOINT}",
                json={
                    "username": username,
                    "password": password,
                    "device_id": self.parent_window.get_device_id()
                },
                verify=Config.VERIFY_SSL,
                timeout=Config.REQUEST_TIMEOUT
            )

            if response.status_code == 200:
                data = response.json()
                self.parent_window.set_auth_tokens(
                    access_token=data["access"],
                    refresh_token=data["refresh"]
                )
                self._handle_successful_login()
            else:
                self._show_error("Benutzername oder Passwort ist falsch")
        except requests.RequestException as e:
            self.logger.error(f"Login failed: {str(e)}")
            self._show_error("Verbindungsfehler")
        finally:
            self._set_loading_state(False)

    # Checked In Overlay Debugging für Login
    # def _handle_successful_login(self) -> None:
    #     """Handle successful login and navigate to next screen"""
    #     self.error_label.set_text("")
    #     self._state = LoginState.SUCCESS
    #
    #     # Show overlay first, then switch page
    #     self.parent_window.show_checked_in_overlay(
    #         "Test User",  # For debugging
    #         lambda: self.parent_window.switch_page("choose_room")  # Callback after overlay
    #     )

    def _handle_successful_login(self) -> None:
        """Handle successful login and navigate to next screen"""
        self.error_label.set_text("")
        self._state = LoginState.SUCCESS
        print("TEST DEBUG")
        # Navigate to room selection after successful login
        GLib.timeout_add(500, self.parent_window.switch_page, "choose_room")

    def _show_error(self, message: str) -> None:
        """Display error message"""
        self.error_label.set_text(message)
        self._state = LoginState.ERROR

    def _set_loading_state(self, is_loading: bool) -> None:
        """Update UI for loading state"""
        self._state = LoginState.LOADING if is_loading else LoginState.IDLE
        self.login_button.set_sensitive(not is_loading)
        self.login_button.set_label("Wird geladen..." if is_loading else "Anmelden")

    def _show_help_dialog(self, button: Gtk.Button) -> None:
        """Show help dialog matching web version"""
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Was muss ich in diesem Anzeigefenster beachten?"
        )
        dialog.format_secondary_text(
            "Hier können Sie sich mit Ihrem Nutzerkonto anmelden. "
            "Falls Sie noch kein Nutzerkonto besitzen, wenden Sie sich an einen Administrator."
        )
        dialog.run()
        dialog.destroy()