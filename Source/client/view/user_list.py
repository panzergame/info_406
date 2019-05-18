# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from core import *
from .observer import *


class UserList(Gtk.VBox):

    SELECTION_ROW = 2
    FIRSTNAME_ROW = 0

    def __init__(self, common):
        Gtk.VBox.__init__(self)
        self.common = common

        self.list = Gtk.ListStore(str, str, bool)

        view = Gtk.TreeView(model=self.list)

        first_name = Gtk.CellRendererText()
        last_name = Gtk.CellRendererText()
        selected = Gtk.CellRendererToggle()

        selected.connect("toggled", self.on_selected)

        name_column = Gtk.TreeViewColumn("Nom")
        select_column = Gtk.TreeViewColumn("Sélectionné(s)", selected, active = 2)

        name_column.pack_start(first_name , True)
        name_column.pack_start(last_name, True)
        name_column.add_attribute(first_name , "text" , 0)
        name_column.add_attribute(last_name, "text", 1)

        view.append_column(name_column)
        view.append_column(select_column)

        self.add(view)

    def on_selected(self ,widget, path):
        self.list[path][UserList.SELECTION_ROW] = not self.list[path][UserList.SELECTION_ROW]
        print(self.list[path][UserList.FIRSTNAME_ROW], self.list[path][UserList.SELECTION_ROW])

    def set_users(self, users):
        self.list.clear()

        for user in users:
            self.list.append((user.first_name, user.last_name, False))
