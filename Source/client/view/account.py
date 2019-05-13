# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *

from .group import *

class AccountBox(Gtk.VBox):

	SELECTION_ROW = 2
	USER_ROW = 3
	FIRSTNAME_ROW = 0

	def __init__(self, common):
		super().__init__()

		self.common = common
		self.common.add_observer(self)

		title = Gtk.Label("Utilisateurs", xalign=0)
		add_user_button = Gtk.Button(label="Ajouter un utilisateur")
		add_user_button.connect("clicked", self.on_add_user_clicked)
		self.pack_start(title, True, True, 0)
		self.pack_start(add_user_button, True, True, 0)

		self.list = Gtk.ListStore(str, str, bool, object)

		view = Gtk.TreeView(model=self.list)

		first_name = Gtk.CellRendererText()
		last_name = Gtk.CellRendererText()

		selected = Gtk.CellRendererToggle()
		selected.connect("toggled", self.on_selected)
		select_column = Gtk.TreeViewColumn("Sélectionné(s)", selected, active=2)

		name_column = Gtk.TreeViewColumn("Nom")
		name_column.pack_start(first_name, True)
		name_column.pack_start(last_name, True)
		name_column.add_attribute(first_name, "text", 0)
		name_column.add_attribute(last_name, "text", 1)

		view.append_column(name_column)
		view.append_column(select_column)
		view.connect("row-activated", self.on_user_changed)

		self.group_list = GroupList(self.common)

		self.add(view)
		supp_up_box = Gtk.Box()
		del_user_button = Gtk.Button(label="Supprimer des utilisateurs")
		del_user_button.connect("clicked", self.on_del_user_clicked)
		up_user_button = Gtk.Button(label="Modifier un utilisateur")
		up_user_button.connect("clicked", self.on_up_user_clicked)
		supp_up_box.add(del_user_button)
		supp_up_box.add(up_user_button)
		self.add(supp_up_box)
		self.add(Gtk.Label("Mes groupes", xalign=0))
		self.add(self.group_list)

		self.update(self.common)

	def on_user_changed(self, model, path, column):
		user = self.list[path][AccountBox.USER_ROW]
		self.common.user_clicked = user
		self.common.agenda_displayed = user.agenda
		self.group_list.set_groups(user.groups)

	def on_add_user_clicked(self, widget):
		print("add")


	def on_del_user_clicked(self, widget):
		print("delete user")
		dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Alerte : Suppression impossible")
		dialog.format_secondary_text("Il doit imperativement rester au moins 1 utilisateur lié à ce compte")

		nb_users = len(self.list)
		nb_selected = 0
		for row in self.list:
			if(row[AccountBox.SELECTION_ROW]):
				nb_selected = nb_selected + 1
		if(not(nb_users == nb_selected)):
			for row in self.list:
				if (row[AccountBox.SELECTION_ROW]):
					row[AccountBox.USER_ROW].delete()
					print(self.common.account)
		else:
			dialog.run()
			dialog.destroy()

		self.common._notify()

	def on_up_user_clicked(self, widget):
		print("modif")

	def on_selected(self, widget, path):
		self.list[path][AccountBox.SELECTION_ROW] = not self.list[path][AccountBox.SELECTION_ROW]
		print(self.list[path][AccountBox.FIRSTNAME_ROW], self.list[path][AccountBox.SELECTION_ROW])

	def update(self, common):

		if self.common.user_clicked is not None:
			self.group_list.set_groups(self.common.user_clicked.groups)

		self.list.clear()
		for user in common.account.users:
			self.list.append((user.first_name, user.last_name, False, user))
