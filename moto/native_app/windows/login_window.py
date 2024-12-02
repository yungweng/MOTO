import gi
import requests
import uuid

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# Globals (optional, could be moved to a config module)
DOMAIN = "https://127.0.0.1:8000"
DEVICE_ID = str(uuid.uuid4())


class LoginWindow(Gtk.Box):
    def __init__(self, parent_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)
        self.parent_window = parent_window

        # Title
        label = Gtk.Label()
        label.set_markup("<span font='26'>Login Page</span>")
        self.pack_start(label, True, True, 0)

        # Username and Password Entry
        self.username = Gtk.Entry()
        self.username.set_placeholder_text("Username")
        self.pack_start(self.username, False, False, 0)

        self.password = Gtk.Entry()
        self.password.set_placeholder_text("Password")
        self.password.set_visibility(False)
        self.pack_start(self.password, False, False, 0)

        # Device ID Entry
        self.device_id_entry = Gtk.Entry()
        self.device_id_entry.set_placeholder_text("Device ID")
        self.pack_start(self.device_id_entry, False, False, 0)

        # Submit Button
        button = Gtk.Button(label="Login")
        button.connect("clicked", self.on_login_clicked)
        self.pack_start(button, False, False, 0)

        # Response Label
        self.response_label = Gtk.Label(label="")
        self.pack_start(self.response_label, True, True, 0)

    def on_login_clicked(self, button):
        """Handle login logic here."""
        username = self.username.get_text()
        password = self.password.get_text()
        device_id = self.device_id_entry.get_text() or DEVICE_ID

        try:
            response = requests.post(
                f"{DOMAIN}/api/login/",
                json={"device_id": device_id, "username": username, "password": password},
                verify=False
            )
            if response.status_code == 200:
                token = response.json().get("access_token")
                self.response_label.set_text("Login successful!")
                # Optionally switch to another page
                # self.parent_window.switch_page("another_page")
            else:
                self.response_label.set_text(f"Login failed: {response.status_code}")
        except requests.RequestException as e:
            self.response_label.set_text(f"Error: {e}")
