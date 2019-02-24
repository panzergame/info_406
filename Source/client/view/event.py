# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class EventBox(Gtk.Box):
	#Boîte d'affichage détaillé d'un évènement
	def __init__(self, common):
		Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
		self.loadSubElements(common.event_clicked)
		common.add_observer(self)

	def loadSubElements(self, event):
		#Nom de l'évènement
		self.name = EventTitleBox(event.type,event.start, event.end)
		self.add(self.name)

 		#Description       
		self.description = EventDescriptionScrollable(event.description)
		self.add(Gtk.Label("Description"))
		self.add(self.description)

 		#Ressources utilisées       
		self.resources = EventResourcesScrollable(event.resources)
		self.add(Gtk.Label("Ressources"))
		self.add(self.resources)

		#Utilisateurs inscrits        
		self.users = EventUsersScrollable(event.users)
		self.add(Gtk.Label("Participants"))
		self.add(self.users)

	def update(self, common):
		#Mis à jour des éléments du widget en fonction du modele
		self.name.update(common.event_clicked.type, common.event_clicked.start, common.event_clicked.end)
		self.description.update(common.event_clicked.description)
		self.resources.update(common.event_clicked.resources)
		self.users.update(common.event_clicked.users)


class EventTitleBox(Gtk.Box):
	#Label d'affichage du type d'un évènement
	def __init__(self, eventType, eventStart, eventEnd):
		Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL)
		self.type = Gtk.Label(label=eventType)
		slot_text = "{:02d}:{:02d} - {:02d}:{:02d}".format(eventStart.hour, eventStart.minute, eventEnd.hour, eventEnd.minute)
		self.slot = Gtk.Label(label = slot_text)
		
		self.add(self.type)
		self.add(self.slot)

	def update(self, eventType, eventStart, eventEnd):
		self.type.set_text(eventType)
		self.slot.set_text("{:02d}:{:02d} - {:02d}:{:02d}".format(eventStart.hour, eventStart.minute, eventEnd.hour, eventEnd.minute))

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