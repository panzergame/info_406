import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class AccountBox(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self,orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_border_width(10)

        title = Gtk.Label("Sélectionner un utilisateur")

        button1 = Gtk.ToggleButton("Utilisateur 1")
        button2 = Gtk.ToggleButton("Utilisateur 2")
        button3 = Gtk.ToggleButton("Utilisateur 3")

        button1.connect("toggled", self.on_button_toggled, "1")
        button2.connect("toggled", self.on_button_toggled, "2")
        button3.connect("toggled", self.on_button_toggled, "3")

        self.pack_start(title, True, True, 0)
        self.pack_start(button1, True, True, 0)
        self.pack_start(button2, True, True, 0)
        self.pack_start(button3, True, True, 0)

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
        else:
            state = "off"
        print("Button", name, "was turned", state)