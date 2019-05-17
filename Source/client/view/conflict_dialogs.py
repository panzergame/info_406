# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from core import *

class SpeConflictDialog(Gtk.Dialog):
	def __init__(self, events_list):
		Gtk.Dialog.__init__(self, "Conflit lors de l'ajout d'un évènement", None, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OK, Gtk.ResponseType.OK))

		self.events_list = events_list

		self.info = Gtk.Label(""" Vous ne pouvez pas ajouter d'évenements sur cette plage horaire car vous êtes indispensables au(x) évènement(s) suivant(s) :""")
		self.choix = Gtk.Label(""" Cliquez sur "Valider" pour déplacer votre nouvel évènement ou sur "Annuler" pour abandonner la création.""")

		self.list = Gtk.ListStore(str)
		view = Gtk.TreeView(model=self.list)
		name = Gtk.CellRendererText()

		name_column = Gtk.TreeViewColumn("Nom :")
		name_column.pack_start(name, True)

		view.append_column(name_column)

		self.list_filling()

		box = self.get_content_area()
		box.add(self.info)
		box.add(view)
		box.add(self.choix)
		self.show_all()

	def list_filling(self):
		for event in self.events_list:
			self.list.append([event.type])