# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *
from .add_event import *
from .common import *


class SpeConflictDialog(Gtk.Dialog):
	def __init__(self, events_list):
		Gtk.Dialog.__init__(self, "Conflit lors de l'ajout d'un évènement", None, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OK, Gtk.ResponseType.OK))

		self.events_list = events_list
		self.info = Gtk.Label(""" Vous ne pouvez pas ajouter d'évènement sur cette plage horaire car vous êtes indispensable aux évènements suivants :""")
		self.choix = Gtk.Label(""" Cliquez sur "Valider" pour déplacer votre nouvel évènement ou sur "Annuler" pour abandonner la création.""")

		self.list = Gtk.ListStore(str, str, str)
		view = Gtk.TreeView(model=self.list)
		name = Gtk.CellRendererText()
		start = Gtk.CellRendererText()
		end = Gtk.CellRendererText()

		name_column = Gtk.TreeViewColumn("Nom :", name, text=0)
		name_column.pack_start(name, True)
		start_column = Gtk.TreeViewColumn("Début :", start, text=1)
		start_column.pack_start(start, True)
		end_column = Gtk.TreeViewColumn("Fin :", end, text=2)
		end_column.pack_start(end, True)

		view.append_column(name_column)
		view.append_column(start_column)
		view.append_column(end_column)

		self.list_filling()

		box = self.get_content_area()
		box.add(self.info)
		box.add(view)
		box.add(self.choix)
		self.show_all()

	def list_filling(self):
		for event in self.events_list:
			deb = datetime_str(event.start)
			fin = datetime_str(event.end)
			self.list.append((event.type, deb, fin))


class StdConflictDialog(Gtk.Dialog):
	def __init__(self, start, end, common):
		Gtk.Dialog.__init__(self, "Conflits lors de l'ajout d'un évènement", None, 0,
			("Abandonner la création", Gtk.ResponseType.CANCEL, "Déplacer l'évènement en cours de création", 2, "Écraser les évènements existants", Gtk.ResponseType.OK))

		self.common = common

		self.start = start
		self.end = end

		#self.add_button("Éditer", 1)

		self.events_list = self.common.agenda_displayed.value.all_events(self.start, self.end)
		self.grp_events = self.events_list - self.common.agenda_displayed.value.events(self.start, self.end)
		self.perso_events = self.events_list - self.grp_events

		self.info = Gtk.Label("""Vous ne pouvez pas ajouter d'évènement sur cette plage horaire car les évènements suivants s'y trouvent déjà :""")
		#self.choix = Gtk.Label(
#	"""Cliquez sur "Valider" pour forcer la création du nouvel évènement sur cette plage horaire et ainsi écraser le(s) évènement(s) déjà existant(s),
#sur "Éditer" pour éditer les évènements déjà présent(s),
#sur "Déplacer" pour déplacer votre nouvel évènement ou sur "Annuler" pour abandonner la création.""")

		box = self.get_content_area()
		box.add(self.info)

		if (self.have_grp_events()):
			self.list_grp = Gtk.ListStore(str, str, str)
			view_grp = Gtk.TreeView(model=self.list_grp)
			name_grp = Gtk.CellRendererText()
			start_grp = Gtk.CellRendererText()
			end_grp = Gtk.CellRendererText()

			name_column_grp = Gtk.TreeViewColumn("Évènements de Groupe :", name_grp, text=0)
			name_column_grp.pack_start(name_grp, True)
			start_grp_column = Gtk.TreeViewColumn("Début :", start_grp, text=1)
			start_grp_column.pack_start(start_grp, True)
			end_grp_column = Gtk.TreeViewColumn("Fin :", end_grp, text=2)
			end_grp_column.pack_start(end_grp, True)

			view_grp.append_column(name_column_grp)
			view_grp.append_column(start_grp_column)
			view_grp.append_column(end_grp_column)

			view_grp.append_column(name_column_grp)

			self.grp_list_filling()

			box.add(view_grp)

		self.list = Gtk.ListStore(str, str, str)
		view = Gtk.TreeView(model=self.list)

		name = Gtk.CellRendererText()
		start = Gtk.CellRendererText()
		end = Gtk.CellRendererText()

		name_column = Gtk.TreeViewColumn("Évènements Perso :", name, text=0)
		name_column.pack_start(name, True)
		start_column = Gtk.TreeViewColumn("Début :", start, text=1)
		start_column.pack_start(start, True)
		end_column = Gtk.TreeViewColumn("Fin :", end, text=2)
		end_column.pack_start(end, True)

		view.append_column(name_column)
		view.append_column(start_column)
		view.append_column(end_column)

		view.append_column(name_column)

		self.list_filling()

		box.add(view)

		#box.add(self.choix)
		self.show_all()

	def list_filling(self):
		for event in self.perso_events:
			deb = datetime_str(event.start)
			fin = datetime_str(event.end)
			self.list.append((event.type, deb, fin))

	def grp_list_filling(self):
		for event in self.grp_events:
			deb = datetime_str(event.start)
			fin = datetime_str(event.end)
			self.list_grp.append((event.type, deb, fin))

	def have_grp_events(self):
		return self.grp_events != set()

class ForceRequestDialog(Gtk.Dialog):
	def __init__(self):
		Gtk.Dialog.__init__(self, "Demande de confirmation", None, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OK, Gtk.ResponseType.OK))

		self.info = Gtk.Label("""	Êtes-vous sûr de vouloir créer cet évènement sur cette plage horaire ?
En faisant cela vous écraserez de manière irréversible tous les évènements existants.""")

		box = self.get_content_area()
		box.add(self.info)
		self.show_all()

class EditEventsDialog(Gtk.Dialog):
	def __init__(self, start, end, common):
		Gtk.Dialog.__init__(self, "Édition d'évènements", None, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OK, Gtk.ResponseType.OK))

		self.common = common

		self.start = start
		self.end = end

		self.events_list = self.common.agenda_displayed.value.all_events(self.start, self.end)
		self.grp_events = self.events_list - self.common.agenda_displayed.value.events(self.start, self.end)
		self.perso_events = self.events_list - self.grp_events

		box = self.get_content_area()

		if (self.have_grp_events()):
			label = Gtk.Label("Évènements de Groupe :")
			self.list_grp = Gtk.ListBox()
			self.dereg = Gtk.Button("Se désinscrire (de tous les groupes correspondants aux évènements ci-dessus)")
			self.dereg.connect("clicked", self.on_dereg_clicked)
			self.grp_list_filling()
			box.add(label)
			box.add(self.list_grp)
			box.add(self.dereg)


		label = Gtk.Label("Évènements Perso :")
		self.list = Gtk.ListBox()
		self.list_filling()
		box.add(label)
		box.add(self.list)
		self.conflicts_counter = Gtk.Label()
		self.compt_conflicts()
		box.add(self.conflicts_counter)
		self.show_all()

	def list_filling(self):
		for event in self.perso_events:
			row = PersonalEventRow(event, self.common)
			self.list.add(row)

	def grp_list_filling(self):
		for event in self.grp_events:
			row = GroupEventRow(event)
			self.list_grp.add(row)

	def have_grp_events(self):
		return self.grp_events != set()

	def compt_conflicts(self):
		nb = len(self.events_list)
		text = "Nombre de conflits restants : " + (str(nb))
		self.conflicts_counter.set_text(text)

	#def on_dereg_clicked(self, button):
		#for event in self.grp_events:

		#self.update()

	def update(self):
		if(len(self.events_list) != 0):
			if (self.have_grp_events()):
				self.grp_list_filling()
			if(self.perso_events != set()):
				self.list_filling()
		self.compt_conflicts()


class PersonalEventRow(Gtk.ListBoxRow):
	def __init__(self, event, common):
		Gtk.ListBoxRow.__init__(self)

		self.common = common

		self.event = event
		self.deb = datetime_str(event.start)
		self.fin = datetime_str(event.end)
		self.nom = event.type

		self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=25)
		name = Gtk.Label(self.nom)
		start = Gtk.Label(self.deb)
		end = Gtk.Label(self.fin)
		#edit = Gtk.Button("Éditer")
		#edit.connect("clicked", self.on_edit_clicked)

		self.hbox.pack_start(name, True, True, 0)
		self.hbox.pack_start(start, True, True, 0)
		self.hbox.pack_start(end, True, True, 0)
		self.hbox.pack_start(edit, True, True, 0)

		self.add(self.hbox)

	"""def on_edit_clicked(self, button):
		button = AddEventButton(self.common)
		button.launch_add_event(self.event)"""

class GroupEventRow(Gtk.ListBoxRow):
	def __init__(self, event):
		Gtk.ListBoxRow.__init__(self)

		self.event = event
		self.deb = datetime_str(event.start)
		self.fin = datetime_str(event.end)
		self.nom = event.type

		self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=25)
		name = Gtk.Label(self.nom)
		start = Gtk.Label(self.deb)
		end = Gtk.Label(self.fin)

		self.hbox.pack_start(name, True, True, 0)
		self.hbox.pack_start(start, True, True, 0)
		self.hbox.pack_start(end, True, True, 0)

		self.add(self.hbox)
