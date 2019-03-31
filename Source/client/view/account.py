# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *

from .group import *

class AccountBox(Gtk.VBox):

	def __init__(self, common):
		super().__init__()

		self.common = common

		title = Gtk.Label("Utilisateurs", xalign=0)
		self.pack_start(title, True, True, 0)

		self.list = Gtk.ListStore(str, str, object)

		view = Gtk.TreeView(self.list)

		first_name = Gtk.CellRendererText()
		last_name = Gtk.CellRendererText()
		name_column = Gtk.TreeViewColumn("Nom")
		name_column.pack_start(first_name, True)
		name_column.pack_start(last_name, True)
		name_column.add_attribute(first_name, "text", 0)
		name_column.add_attribute(last_name, "text", 1)

		view.append_column(name_column)

		select = view.get_selection()
		select.connect("changed", self.on_user_changed)

		self.group_list = GroupList(self.common)

		self.add(view)
		self.add(Gtk.Label("Groupes", xalign=0))
		self.add(self.group_list)

		for user in common.account.users:
			self.list.append((user.first_name, user.last_name, user))

	def on_user_changed(self, selection):
		model, iter = selection.get_selected()
		if iter is not None:
			user = model[iter][2]
			self.common.user_clicked = user
			self.common.agenda_displayed = user.agenda
			self.group_list.set_groups(user.groups)

	def update(self, common):
		self.group_list.set_groups(self.common.user_clicked.groups)
