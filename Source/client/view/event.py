# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .common import *
from .observer import *
from datetime import *
from .add_event import *

class EventBox(Gtk.ListBox, ViewObserver):
	#Boîte d'affichage détaillé d'un évènement
	def __init__(self, common):
		Gtk.ListBox.__init__(self)
		ViewObserver.__init__(self, common, common.event_clicked, common.agenda_displayed)

		self.initSubElements()

	def initSubElements(self):
		#Initialise les sous éléments avec des valeurs par défauts
		#Nom de l'évènement

		self.name = EventTitleBox()
		#Date
		self.date = EventDateBox()
 		#Description       
		self.description = EventDescriptionScrollable("default_description")
 		#Ressources utilisées       
		self.resources = EventResourcesScrollable()
		#Utilisateurs inscrits
		self.users = EventUsersScrollable()

		row = Gtk.ListBoxRow()
		box = Gtk.HBox()
		box.add(Gtk.Label("Type", xalign=0))
		box.add(self.name)
		row.add(box)
		self.add(row)

		row = Gtk.ListBoxRow()
		box = Gtk.HBox()
		box.add(Gtk.Label("Date", xalign=0))
		box.add(self.date)
		row.add(box)
		self.add(row)

		row = Gtk.ListBoxRow()
		box = Gtk.HBox()
		box.add(Gtk.Label("Description", xalign=0))
		box.add(self.description)
		row.add(box)
		self.add(row)

		row = Gtk.ListBoxRow()
		box = Gtk.HBox()
		box.add(Gtk.Label("Ressources", xalign=0))
		box.add(self.resources)
		row.add(box)
		self.add(row)

		row = Gtk.ListBoxRow()
		box = Gtk.HBox()
		box.add(Gtk.Label("Participants", xalign=0))
		box.add(self.users)
		row.add(box)
		self.add(row)

		button = Gtk.Button("Modifier")
		button.connect("clicked", self.on_modify_clicked)
		self.add(button)

		self.supp_button = Gtk.Button("Supprimer")
		self.supp_button.connect("clicked", self.on_delete_clicked)
		self.add(self.supp_button)


	def on_delete_clicked(self, button):
		self.common.event_clicked.value[self.common.agenda_displayed.value].delete()
		self.common.event_clicked.value[self.common.agenda_displayed.value] = None

	def on_modify_clicked(self, button):
		ex = self.common.event_clicked.value[self.common.agenda_displayed.value]
		self.modify_event(ex)

	def modify_event(self, event):
		button = AddEventButton(self.common)
		button.launch_add_event(event)


	def update(self):
		ev = self.common.event_clicked.value.get(self.common.agenda_displayed.value, None)
		#.get(self.common.agenda_displayed.value, None)
		#Mis à jour des éléments du widget en fonction du modele
		if ev is None:
			self.hide()
		else:
			#Si on change d'évènement, on mets à jour les sous éléments
			self.show()
			self.name.update(ev.type)
			self.date.update(ev.start, ev.end)
			self.description.update(ev.description)
			self.resources.update(ev.resources)
			self.users.update(ev.users)

class EventTitleBox(Gtk.Label):
	#Label d'affichage du type d'un évènement

	def __init__(self):
		super().__init__(label="default")

	def update(self, eventType):
		self.set_text(eventType)

class EventDateBox(Gtk.Label):
	def __init__(self):
		super().__init__(label="default")

	def update(self, start, end):
		self.set_text(event_to_date_str(start, end))

class EventDescriptionScrollable(Gtk.ScrolledWindow):
	#Fenêtre défilable, contient la description d'un évènement
	def __init__(self, description):
		Gtk.ScrolledWindow.__init__(self)  
		self.label = Gtk.Label()
		self.label.set_line_wrap(True)
		self.label.set_text(description)
		self.set_property("expand",True)
		self.add(self.label)

	def update(self, description):
		self.label.set_text(description)

class EventResourcesScrollable(Gtk.TreeView):
	def __init__(self):
		self.list = Gtk.ListStore(str, str, int, object)

		Gtk.TreeView.__init__(self, self.list)

		name_column = Gtk.TreeViewColumn("Nom", Gtk.CellRendererText(), text=0)
		loc_column = Gtk.TreeViewColumn("Location", Gtk.CellRendererText(), text=1)
		cap_column = Gtk.TreeViewColumn("Capacité", Gtk.CellRendererText(), text=2)

		self.append_column(name_column)
		self.append_column(loc_column)
		self.append_column(cap_column)

	def update(self, resources):
		self.list.clear()

		for res in resources:
			self.list.append((res.name, res.location, res.capacity, res))

class EventUsersScrollable(Gtk.TreeView):
	def __init__(self):
		self.list = Gtk.ListStore(str, str, object)

		Gtk.TreeView.__init__(self, self.list)

		fname_column = Gtk.TreeViewColumn("Prénom", Gtk.CellRendererText(), text=0)
		lname_column = Gtk.TreeViewColumn("Nom", Gtk.CellRendererText(), text=1)

		self.append_column(fname_column)
		self.append_column(lname_column)

	def update(self, users):
		self.list.clear()

		for user in users:
			self.list.append((user.first_name, user.last_name, user))
