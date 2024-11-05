import gi
import requests
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Mein GTK-Fenster")

        self.set_decorated(False)

        self.fullscreen()

        # Verbinde das Schließen-Ereignis
        self.connect("destroy", Gtk.main_quit)

        self.connect("key-press-event", self.on_key_press)
        self.test()

        # Zeige das Fenster an
        self.show_all()

    def test(self):
        # Erstelle eine vertikale Box, die das Label zentriert ausrichtet
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_halign(Gtk.Align.CENTER)  # Zentriert die Box horizontal
        box.set_valign(Gtk.Align.CENTER)  # Zentriert die Box vertikal

        # Erstelle das Label und setze den Text
        label = Gtk.Label()
        label.set_markup("<span font='26'>MotoApp</span>")

        label.set_justify(Gtk.Justification.CENTER)

        # Füge das Label zur Box hinzu
        box.pack_start(label, True, True, 0)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Gib hier die ID ein...")
        self.entry.set_size_request(200, 30)
        box.pack_start(self.entry, True, True, 0)

        self.response_label = Gtk.Label(label="")
        self.response_label.set_justify(Gtk.Justification.CENTER)
        box.pack_start(self.response_label, True, True, 0)

        # Füge die Box zum Fenster hinzu
        self.add(box)
    
    def on_key_press(self, widget, event):
        # Überprüfe, ob die ESC-Taste gedrückt wurde
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()
        elif event.keyval == Gdk.KEY_Return:
            input_text = self.entry.get_text()  # Text aus dem Eingabefeld holen
            self.entry.set_text("")
            self.make_request(input_text=input_text)
    
    def make_request(self, input_text):
        try:
            response = requests.get("https://127.0.0.1:8000/api/get_name_of_id/" + input_text + "/", verify=False, allow_redirects=True)  # URL deines Django-Servers
            if response.status_code == 200:
                response_data = response.json()  # Konvertiere die Antwort in ein JSON-Objekt
                self.response_label.set_text(response_data.get("message", "Keine Nachricht erhalten."))
            else:
                self.response_label.set_text(f"Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print("HTTP Request failed:", e)

if __name__ == "__main__":
    # Initialisiere GTK
    win = MainWindow()
    Gtk.main()