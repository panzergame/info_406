# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from core import *

class AddUserDialog(Gtk.Dialog):
	def __init__(self):
		Gtk.Dialog.__init__(self, "Ajouter un utilisateur", None, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OK, Gtk.ResponseType.OK))

		self.name = Gtk.Label("Nom :  *")
		self.first_name = Gtk.Label("Prénom :  *")
		self.mail = Gtk.Label("Adresse mail : ")
		self.tel = Gtk.Label("N° téléphone : ")
		self.info = Gtk.Label("Les champs marqués d'un '*' sont obligatoires.")

		self.name_entry = Gtk.Entry()
		self.first_name_entry = Gtk.Entry()
		self.mail_entry = Gtk.Entry()
		self.tel_entry = Gtk.Entry()

		grid = Gtk.Grid()

		grid.add(self.name)
		grid.attach(self.name_entry, 1, 0, 1, 1)
		grid.attach(self.first_name, 0, 1, 1, 1)
		grid.attach(self.first_name_entry, 1 , 1, 1, 1)
		grid.attach(self.mail, 0, 2, 1, 1)
		grid.attach(self.mail_entry, 1, 2, 1, 1)
		grid.attach(self.tel, 0, 3, 1, 1)
		grid.attach(self.tel_entry, 1, 3, 1, 1)
		grid.attach(self.info, 0, 4, 2, 1)

		box = self.get_content_area()
		box.add(grid)
		self.show_all()

	def est_vide(self, chaine):
		if (len(chaine) == 0):
			res = True
		else:
			res = True
			for i in range(0,len(chaine)):
				if (chaine[i]!=' '):
					res = False
		return res


	def get_name(self):
		return self.name_entry.get_text()

	def get_first_name(self):
		return self.first_name_entry.get_text()

	def get_mail(self):
		return self.mail_entry.get_text()

	def get_tel(self):
		return self.tel_entry.get_text()

