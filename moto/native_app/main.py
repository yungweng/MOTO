import gi
from typing import Optional
from view.login import LoginWindow
from view.choose_room import Choose_RoomWindow
from view.create_activity import CreateActivityWindow
from view.home import HomeWindow
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Main Application")
        self.set_default_size(1280, 720)

        # Placeholder for authentication tokens
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None

        # Main container for switching views
        self.main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  # Renamed to avoid conflict
        self.add(self.main_container)

        # Initialize first page based on authentication
        if self.user_is_authenticated():
            self.switch_page("choose_room")
        else:
            self.switch_page("login")

    def user_is_authenticated(self) -> bool:
        """Check if the user is authenticated based on access token."""
        return self.access_token is not None

    def set_auth_tokens(self, access_token: str, refresh_token: str):
        """Set the authentication tokens after successful login."""
        self.access_token = access_token
        self.refresh_token = refresh_token

    def get_device_id(self) -> str:
        """Generate or return a unique device identifier."""
        # Placeholder for a device ID; in production, use a persistent unique identifier
        return "default-device-id"

    def switch_to_choose_room(self):
        # Clear existing children
        for child in self.main_container.get_children():
            self.main_container.remove(child)

        # Add the Choose_RoomWindow
        choose_room_view = Choose_RoomWindow(self)
        self.main_container.add(choose_room_view)
        self.main_container.show_all()

    def switch_to_create_activity(self, room_id):
        # Clear existing children
        for child in self.main_container.get_children():
            self.main_container.remove(child)

        # Add the CreateActivityWindow
        create_activity_view = CreateActivityWindow(self, room_id)
        self.main_container.add(create_activity_view)
        self.main_container.show_all()

    def switch_to_home(self, room_id: str) -> None:
        """Switch to home view"""
        # Clear existing children
        for child in self.main_container.get_children():
            self.main_container.remove(child)

        # Create new home page with room_id
        home_window = HomeWindow(self, room_id)
        self.main_container.add(home_window)
        self.main_container.show_all()

    def switch_page(self, page_name: str):
        """Switch the current view to the specified page."""
        # Clear existing children from the container
        for child in self.main_container.get_children():
            self.main_container.remove(child)

        if page_name == "login":
            self.main_container.add(LoginWindow(parent_window=self))
        elif page_name == "choose_room":
            self.main_container.add(Choose_RoomWindow(parent_window=self))
        else:
            raise ValueError(f"Unknown page name: {page_name}")

        self.main_container.show_all()

if __name__ == "__main__":
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
