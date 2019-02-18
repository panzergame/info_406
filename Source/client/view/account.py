import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *
from client.model.common import *


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
        group = None
        for user in users:
            name = user.first_name + " " + user.last_name
            if first:
                button = Gtk.RadioButton.new_with_label_from_widget(None, name)
                first = False
                group = button
                self.common.set_user_clicked(user)
            else:
                button = Gtk.RadioButton.new_with_label_from_widget(group, name)
            button.connect("toggled", self.on_button_toggled, user)
            self.pack_start(button, False, False, 0)


    def on_button_toggled(self, button, user):

        if button.get_active():
            self.common.set_user_clicked(user)

