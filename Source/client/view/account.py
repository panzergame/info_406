import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *


class AccountBox(Gtk.Box):
    def __init__(self):

        self.account = account

        Gtk.Box.__init__(self,orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_border_width(10)

        title = Gtk.Label("Sélectionner un utilisateur")

        users = account.users
        for user in users:
            name = user.__repr__()
            button = Gtk.ToggleButton(name)
            button.connect("toggled", self.on_button_toggled(id=user.id))


    def on_button_toggled(self, button, id):

        if button.get_active():
            state = id
        else:
            state = id