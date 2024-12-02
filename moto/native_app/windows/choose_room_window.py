import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Choose_RoomWindow(Gtk.Box):
    def __init__(self, parent_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.set_halign(Gtk.Align.FILL)
        self.set_valign(Gtk.Align.FILL)
        self.set_spacing(10)

        # Header Section
        header = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.pack_start(header, False, False, 0)

        big_heading = Gtk.Label(label="Hallo.\nBitte ordne dem Gerät\n einen Raum zu.")
        big_heading.set_name("big_heading")
        header.pack_start(big_heading, False, False, 0)

        # Separator Line
        separator = Gtk.Separator()
        self.pack_start(separator, False, False, 0)

        # Room List Section
        rooms = [
            {"room_number": "1.0", "is_occupied": False},
            {"room_number": "1.1", "is_occupied": False},
            {"room_number": "1.2", "is_occupied": False},
            {"room_number": "1.3", "is_occupied": True},
            {"room_number": "2.0", "is_occupied": False},
        ]

        for room in rooms:
            self.add_room(room["room_number"], room["is_occupied"])

    def add_room(self, room_number, is_occupied):
        """Adds a room entry to the list."""
        room_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        room_box.set_name("room_box")
        room_box.set_halign(Gtk.Align.FILL)
        room_box.set_valign(Gtk.Align.CENTER)

        # Room Number
        room_label = Gtk.Label(label=f"Raum {room_number}")
        room_label.set_name("room_label")
        room_label.set_halign(Gtk.Align.START)
        room_label.set_valign(Gtk.Align.CENTER)
        room_box.pack_start(room_label, True, True, 0)

        # Button: Belegt / Auswählen
        if is_occupied:
            button = Gtk.Button(label="Belegt")
            button.set_name("occupied_button")
        else:
            button = Gtk.Button(label="Auswählen")
            button.set_name("select_button")
            button.connect("clicked", self.on_room_select, room_number)

        room_box.pack_end(button, False, False, 0)
        self.pack_start(room_box, False, False, 0)

    def on_room_select(self, button, room_number):
        """Handles room selection."""
        print(f"Raum {room_number} wurde ausgewählt.")
