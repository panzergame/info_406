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
		ViewObserver.__init__(self, common, common.event_clicked)

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
		self.resources = EventResourcesScrollable([])
		#Utilisateurs inscrits
		self.users = EventUsersScrollable([])

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
		self.common.event_clicked.value.delete()
		self.common.event_clicked.value = None

	def on_modify_clicked(self, button):
		ex = self.common.event_clicked.value
		button = AddEventButton(self.common)
		button.launch_add_event()
		ex.delete()


	def update(self):
		ev = self.common.event_clicked.value
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

class EventResourcesScrollable(Gtk.ScrolledWindow):
	#Fenêtre défilable, contient les ressources d'un évènement
	def __init__(self, resources):
		Gtk.ScrolledWindow.__init__(self)
		resourcesFlowBox = Gtk.FlowBox(orientation = Gtk.Orientation.HORIZONTAL)
		resourcesFlowBox.set_selection_mode(Gtk.SelectionMode.NONE)
		self.add(resourcesFlowBox)
		for resource in resources:
			resourcesFlowBox.add(EventResourceBox(resource))

	def update(self, resources):
		for child in self.get_child().get_children():
			self.get_child().remove(child)
			
		for resource in resources:
			self.get_child().add(EventResourceBox(resource))

class EventResourceBox(Gtk.Box):
	#Boîte d'affichage d'une ressource
	def __init__(self, resource):
		Gtk.Box.__init__(self)

		frame = Gtk.Frame()
		subBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
		title = Gtk.Label(label = "{} ({})".format(resource.name,resource.capacity))
		location = Gtk.Label(label = resource.location)
		subBox.add(title)
		subBox.add(location)

		frame.add(subBox)
        
		self.add(frame)


class EventUsersScrollable(Gtk.ScrolledWindow):
	#Fenêtre défilable, contient les utilisateurs participant à un évènement
	def __init__(self, users):
		Gtk.ScrolledWindow.__init__(self)
		usersFlowBox = Gtk.FlowBox(orientation = Gtk.Orientation.HORIZONTAL)
		usersFlowBox.set_selection_mode(Gtk.SelectionMode.NONE)
		self.add(usersFlowBox)
		for user in users:
			usersFlowBox.add(EventUserBox(user))

	def update(self, users):
		for child in self.get_child().get_children():
			self.get_child().remove(child)
			
		for user in users:
			self.get_child().add(EventUserBox(user))

class EventUserBox(Gtk.Box):
	#Boîte d'affichage d'un utilisateur
	def __init__(self, user):
		Gtk.Box.__init__(self)
		frame = Gtk.Frame()
		frame.add(Gtk.Label(label="{} {}".format(user.first_name, user.last_name)))
		self.add(frame)
