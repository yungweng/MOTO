import gi
from windows.login_window import LoginWindow
from windows.choose_room_window import Choose_RoomWindow
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="MOTO")
        self.set_default_size(1280, 720)
        self.connect("destroy", Gtk.main_quit)

        # Stack for managing multiple pages
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(500)

        # Add pages
        login_window = LoginWindow(self)
        choose_room_window = Choose_RoomWindow(self)
        self.stack.add_named(choose_room_window, "choose_room")
        self.stack.add_named(login_window, "login_window")

        # Add stack to the window
        self.add(self.stack)

        # Apply CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("css/style.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self.show_all()

    def switch_page(self, page_name):
        """Switch to a different page in the stack."""
        self.stack.set_visible_child_name(page_name)


if __name__ == "__main__":
    win = MainWindow()
    Gtk.main()
