import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Source.core import *


class AccountBox(Gtk.Box):

    def __init__(self, account):

        self.account = account

        Gtk.Box.__init__(self,orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_border_width(10)

        title = Gtk.Label("Sélectionner un utilisateur")
        self.pack_start(title, True, True, 0)

        users = account.users
        for user in users:
            name = user.first_name + " " + user.last_name
            id = user.id
            button = Gtk.ToggleButton(name)
            button.connect("toggled", self.on_button_toggled)
            self.pack_start(button, True, True, 0)


    def on_button_toggled(self, button):

        if button.get_active():
            state = "on"
        else:
            state = "off"