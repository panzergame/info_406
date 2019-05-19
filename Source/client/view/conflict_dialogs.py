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

		self.info = Gtk.Label(""" Vous ne pouvez pas ajouter d'évenement sur cette plage horaire car vous êtes indispensables au(x) évènement(s) suivant(s) :""")
		self.choix = Gtk.Label(""" Cliquez sur "Valider" pour déplacer votre nouvel évènement ou sur "Annuler" pour abandonner la création.""")

		self.list = Gtk.ListStore(str)
		view = Gtk.TreeView(model=self.list)
		name = Gtk.CellRendererText()

		name_column = Gtk.TreeViewColumn("Nom :", name, text=0)
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


class StdConflictDialog(Gtk.Dialog):
	def __init__(self, start, end, common):
		Gtk.Dialog.__init__(self, "Conflit lors de l'ajout d'un évènement", None, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

		self.common = common
		self.start = start
		self.end = end

		self.add_button("Éditer", 1)
		self.add_button("Déplacer", 2)
		self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)

		self.events_list = self.common.agenda_displayed.value.all_events(self.start, self.end)
		self.grp_events = self.events_list - self.common.agenda_displayed.value.events(self.start, self.end)
		self.perso_events = self.events_list - self.grp_events

		self.info = Gtk.Label("""Vous ne pouvez pas ajouter d'évenement sur cette plage horaire car le(s) évènement(s) suivant(s) s'y trouve(nt) déjà :""")
		self.choix = Gtk.Label(
			"""Cliquez sur "Valider" pour forcer la création du nouvel évènement sur cette plage horaire et ainsi écraser le(s) évènement(s) déjà existant(s),
sur "Éditer" pour éditer les évènements déjà présent(s),
sur "Déplacer" pour déplacer votre nouvel évènement ou sur "Annuler" pour abandonner la création.""")

		box = self.get_content_area()
		box.add(self.info)

		if (self.have_grp_events()):
			self.list_grp = Gtk.ListStore(str)
			view_grp = Gtk.TreeView(model=self.list_grp)
			name_grp = Gtk.CellRendererText()

			name_column_grp = Gtk.TreeViewColumn("Évènements de Groupe :", name_grp, text=0)
			name_column_grp.pack_start(name_grp, True)

			view_grp.append_column(name_column_grp)

			self.grp_list_filling()

			box.add(view_grp)

		self.list = Gtk.ListStore(str)
		view = Gtk.TreeView(model=self.list)
		name = Gtk.CellRendererText()

		name_column = Gtk.TreeViewColumn("Évènements perso :", name, text=0)
		name_column.pack_start(name, True)

		view.append_column(name_column)

		self.list_filling()

		box.add(view)

		box.add(self.choix)
		self.show_all()

	def list_filling(self):
		for event in self.perso_events:
			self.list.append([event.type])

	def grp_list_filling(self):
		for event in self.grp_events:
				self.list_grp.append([event.type])

	def have_grp_events(self):
		return self.grp_events != set()

class ForceRequestDialog(Gtk.Dialog):
	def __init__(self):
		Gtk.Dialog.__init__(self, "Demande de confirmation", None, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OK, Gtk.ResponseType.OK))

		self.info = Gtk.Label("""	Etes-vous sûr de vouloir créer cet évènement sur cette plage horaire ?
En faisant cela vous écraserez tous les évènements y éxistants de manière irréversible.""")

		box = self.get_content_area()
		box.add(self.info)
		self.show_all()

class EditRequestDialog(Gtk.Dialog):
	def __init__(self):
		Gtk.Dialog.__init__(self, "Demande de confirmation", None, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OK, Gtk.ResponseType.OK))

		self.info = Gtk.Label("""	Etes-vous sûr de vouloir procéder aux changements ?
Les changements opérés seront irréversibles.""")

		box = self.get_content_area()
		box.add(self.info)
		self.show_all()