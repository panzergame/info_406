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
		self.common.add_observer(self)

		title = Gtk.Label("Utilisateurs", xalign=0)
		add_user_button = Gtk.Button(label="Ajouter")
		add_user_button.connect("clicked", self.on_add_user_clicked)
		self.pack_start(title, True, True, 0)
		self.pack_start(add_user_button, True, True, 0)

		self.list = Gtk.ListStore(str, str, object)

		view = Gtk.TreeView(self.list)

		selected = Gtk.CellRendererToggle()
		first_name = Gtk.CellRendererText()
		last_name = Gtk.CellRendererText()
		name_column = Gtk.TreeViewColumn("Nom")
		name_column.pack_start(first_name, True)
		name_column.pack_start(last_name, True)
		name_column.pack_start(selected, True)
		name_column.add_attribute(first_name, "text", 0)
		name_column.add_attribute(last_name, "text", 1)

		view.append_column(name_column)
		view.connect("row-activated", self.on_user_changed)

		self.group_list = GroupList(self.common)

		self.add(view)
		del_user_button = Gtk.Button(label="Supprimer")
		del_user_button.connect("clicked", self.on_del_user_clicked)
		up_user_button = Gtk.Button(label="Modifier")
		up_user_button.connect("clicked", self.on_up_user_clicked)
		self.add(del_user_button)
		self.add(up_user_button)
		self.add(Gtk.Label("Mes groupes", xalign=0))
		self.add(self.group_list)

		for user in common.account.users:
			self.list.append((user.first_name, user.last_name, user))

	def on_user_changed(self, model, path, column):
		user = self.list[path][2]
		self.common.user_clicked = user
		self.common.agenda_displayed = user.agenda
		self.group_list.set_groups(user.groups)

	def on_add_user_clicked(self, widget):
		print("add")

	def on_del_user_clicked(self, widget):
		print("supp")
	def on_up_user_clicked(self, widget):
		print("modif")
	def update(self, common):
		self.group_list.set_groups(self.common.user_clicked.groups)
