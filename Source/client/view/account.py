# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *
from .delete_user_dialog import *
from .add_user_dialog import *
from .supp_confirm_dialog import *
from .modif_user_dialog import *
from .observer import *
from .group_list import *

class AccountBox(Gtk.VBox, ViewObserver):
	SELECTION_ROW = 2
	USER_ROW = 3
	FIRSTNAME_ROW = 0

	def __init__(self, common):
		Gtk.VBox.__init__(self)
		ViewObserver.__init__(self, common, common.user_clicked, common.account)

		title = Gtk.Label()
		title.set_markup("\n <big> Utilisateurs </big> \n")
		self.pack_start(title, True, True, 0)

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

		add_user_button = Gtk.Button(label="Ajouter un utilisateur")
		add_user_button.connect("clicked", self.on_add_user_clicked)

		del_user_button = Gtk.Button(label="Supprimer des utilisateurs")
		del_user_button.connect("clicked", self.on_del_user_clicked)
		up_user_button = Gtk.Button(label="Modifier un utilisateur")
		up_user_button.connect("clicked", self.on_up_user_clicked)

		supp_up_box = Gtk.Box()
		supp_up_box.add(del_user_button)
		supp_up_box.add(up_user_button)


		self.add(view)
		self.pack_start(add_user_button, True, True, 0)
		self.add(supp_up_box)


		groupe = Gtk.Label()
		groupe.set_markup("\n <big> Mes Groupes </big> \n")
		self.add(groupe)
		self.add(self.group_list)

	def on_user_changed(self, model, path, column):
		user = self.list[path][AccountBox.USER_ROW]
		self.common.user_clicked.value = user
		self.common.agenda_displayed.value = user.agenda
		self.group_list.set_groups(user.groups)

	def on_add_user_clicked(self, widget):
		dialog = AddUserDialog()
		valide = False
		while (not(valide)):
			if (dialog.run() == Gtk.ResponseType.OK):
				name = dialog.get_name()
				first_name = dialog.get_first_name()
				email = dialog.get_mail()
				tel = dialog.get_tel()

				if ((dialog.est_vide(name))or(dialog.est_vide(first_name))):
					err = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
											   "Alerte : Création impossible")
					err.format_secondary_text("Des champs obligatoires n'ont pas été remplis,"
											  " veillez à remplir tous les champs marqués d'un '*'.")
					err.run()
					err.destroy()
				else:
					user = User.new(self.common.collection, first_name.replace(" ",""), name.replace(" ",""),
									email.replace(" ",""), tel.replace(" ",""))
					ag = Agenda.new(self.common.collection, "Personnel")
					user.agenda = ag
					self.common.account.value.add_user(user)
					self.common.account.notify()
					valide = True
			else:
				valide = True
		dialog.destroy()


	# Suppression d'utilisateur :
	def on_del_user_clicked(self, widget):
		nb_users = len(self.list)
		nb_selected = 0
		for row in self.list:
			if(row[AccountBox.SELECTION_ROW]):
				nb_selected = nb_selected + 1
		if (nb_selected != 0):
			# Si il reste au moins un utilisateur on procède à la suppression :
			if(not(nb_users == nb_selected)):
				# Appel du dialog de confirmation :
				dia = SuppConfirmDialog()
				if dia.run() == Gtk.ResponseType.OK:
					for row in self.list:
						if (row[AccountBox.SELECTION_ROW]):
							row[AccountBox.USER_ROW].delete()
				self.common.user_clicked.notify()
				dia.destroy()
			else:
				dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
										   "Alerte : Suppression impossible")
				dialog.format_secondary_text("Il doit imperativement rester au moins 1 utilisateur lié à ce compte")
				dialog.run()
				dialog.destroy()


	def on_up_user_clicked(self, widget):
		nb_selected = 0
		for row in self.list:
			if (row[AccountBox.SELECTION_ROW]):
				nb_selected = nb_selected + 1
		if (nb_selected != 0):
			if(nb_selected == 1):
				for row in self.list:
					if (row[AccountBox.SELECTION_ROW]):
						user = row[AccountBox.USER_ROW]
				dialog = ModifUserDialog(user)
				valide = False
				while (not (valide)):
					if (dialog.run() == Gtk.ResponseType.OK):
						name = dialog.get_name().replace(" ","")
						first_name = dialog.get_first_name().replace(" ","")
						email = dialog.get_mail().replace(" ","")
						tel = dialog.get_tel().replace(" ","")
						if ((dialog.est_vide(name)) or (dialog.est_vide(first_name))):
							err = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
													"Alerte : Modification impossible")
							err.format_secondary_text("Des champs obligatoires sont vides,"
													  " veillez à remplir tous les champs marqués d'un '*'.")
							err.run()
							err.destroy()
						else:
							user.first_name = first_name
							user.last_name = name
							user.email = email
							user.tel = tel
							self.common.account.notify()
							valide = True
					else:
						valide = True
				dialog.destroy()
			else:
				dia = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
										   "Alerte : Action impossible")
				dia.format_secondary_text("Vous ne pouvez modifier qu'un utilisateur à la fois.")
				dia.run()
				dia.destroy()


	def on_selected(self, widget, path):
		self.list[path][AccountBox.SELECTION_ROW] = not self.list[path][AccountBox.SELECTION_ROW]
		print(self.list[path][AccountBox.FIRSTNAME_ROW], self.list[path][AccountBox.SELECTION_ROW])

	def update(self):
		user = self.common.user_clicked.value
		if user is not None:
			self.group_list.set_groups(user.groups)

		self.list.clear()
		for user in self.common.account.value.users:
			self.list.append((user.first_name, user.last_name, False, user))
