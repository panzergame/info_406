import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Source.core import *
from Source.client.model.common import *


class AccountBox(Gtk.Box):

    def __init__(self, account, common):

        self.account = account
        self.common = common

        Gtk.Box.__init__(self,orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_border_width(10)

        title = Gtk.Label("Sélectionner un utilisateur")
        self.pack_start(title, True, True, 0)

        users = account.users
        first = True
        for user in users:
            name = user.first_name + " " + user.last_name
            button = Gtk.ToggleButton(name)
            button.connect("toggled", self.on_button_toggled, user)
            self.pack_start(button, True, True, 0)
            if first:
                button.set_active(True)
                first = False


    def on_button_toggled(self, button, user):

        if button.get_active():
            self.common.set_user_clicked(user)
        else:
            state = "off"