import gi
from typing import Optional

from view.login import LoginWindow
from view.choose_room import Choose_RoomWindow
from view.create_activity import CreateActivityWindow
from view.home import HomeWindow
from view.checked_in_overlay import CheckedInOverlay
from view.checked_out_overlay import CheckedOutOverlay
from view.go_home import GoHomeWindow
from view.leave_room_overlay import LeaveRoomOverlay
from view.set_nfc_scan_overlay import SetNFCScanOverlay
from view.master_tablet import MasterTabletWindow
from view.set_nfc_set import SetNFCSetWindow
from view.remove_tablet_overlay import RemoveTabletOverlay
from view.change_roomdata import ChangeRoomDataWindow

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Main Application")
        self.set_default_size(1280, 720)
        self.set_resizable(False)
        # Placeholder for Tag ID
        self.tag_id = "tag_id_string"
        # Placeholder for Room ID
        self.current_room_id = "room_id_string"
        self.fullscreen()

        # Placeholder for authentication tokens
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None

        # Create an overlay container for the main content
        self.overlay_container = Gtk.Overlay()
        self.add(self.overlay_container)

        # Main container for switching views
        self.main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.overlay_container.add(self.main_container)

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
        return "default-device-id"

    def show_checked_in_overlay(self, user_name: str, callback: Optional[callable] = None) -> None:
        """Show the checked-in overlay with user name"""
        overlay = CheckedInOverlay(self, user_name, callback)
        self.overlay_container.add_overlay(overlay)
        self.overlay_container.show_all()

    def show_checked_out_overlay(self, user_name: str, callback: Optional[callable] = None) -> None:
        """Show the checked-out overlay with user name"""
        overlay = CheckedOutOverlay(self, user_name, callback)
        self.overlay_container.add_overlay(overlay)
        self.overlay_container.show_all()

    def show_leave_room_overlay(self, user_name: str) -> None:
        overlay = LeaveRoomOverlay(self, user_name)
        self.overlay_container.add_overlay(overlay)
        self.overlay_container.show_all()

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

    def switch_to_go_home(self):
        """Switch to go home view"""
        for child in self.main_container.get_children():
            self.main_container.remove(child)

        go_home_view = GoHomeWindow(self)
        self.main_container.add(go_home_view)
        self.main_container.show_all()

    def show_remove_tablet_overlay(self) -> None:
        overlay = RemoveTabletOverlay(self)
        self.overlay_container.add_overlay(overlay)
        self.overlay_container.show_all()

    def switch_page(self, page_name: str):
        """Switch the current view to the specified page."""
        # Clear existing children from the container
        for child in self.main_container.get_children():
            self.main_container.remove(child)

        if page_name == "login":
            self.main_container.add(LoginWindow(parent_window=self))
        elif page_name == "choose_room":
            self.main_container.add(Choose_RoomWindow(parent_window=self))
        elif page_name == "home":  # only for development
            self.main_container.add(HomeWindow(parent_window=self, room_id="2"))  # only for development
        elif page_name == "go_home":
            self.main_container.add(GoHomeWindow(parent_window=self))
        elif page_name == "checked_in":
            self.main_container.add(CheckedInOverlay(parent_window=self, user_name="Namensgebende Grüße"))
        elif page_name == "checked_out":
            self.main_container.add(CheckedOutOverlay(parent_window=self, userchang_name="Yannick Wenger"))
        elif page_name == "go_home":
            self.main_container.add(GoHomeWindow(parent_window=self))
        elif page_name == "set_nfc_scan":
            self.main_container.add(SetNFCScanOverlay(parent_window=self))
        elif page_name == "master_tablet":
            self.main_container.add(MasterTabletWindow(parent_window=self))
        elif page_name == "set_nfc_set":
            self.main_container.add(SetNFCSetWindow(parent_window=self, tag_id=self.tag_id))
        elif page_name == "change_roomdata":
            self.main_container.add(ChangeRoomDataWindow(parent_window=self, room_id=self.current_room_id))
        elif page_name == "leave_room_overlay":
            self.main_container.add(LeaveRoomOverlay(parent_window=self, user_name="Namensgebende Grüße"))
        elif page_name == "master_tablet":
            self.main_container.add(MasterTabletWindow(parent_window=self))
        elif page_name == "set_nfc_scan_overlay":
            self.main_container.add(SetNFCScanOverlay(parent_window=self))
        else:
            raise ValueError(f"Unknown page name: {page_name}")

        self.main_container.show_all()

if __name__ == "__main__":
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()