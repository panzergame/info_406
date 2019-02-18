# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class EventBox(Gtk.Box):
    #Boîte d'affichage détaillé d'un évènement
    def __init__(self, event):
        Gtk.Box.__init__(self, spacing=10, orientation=Gtk.Orientation.VERTICAL)
        self.loadSubElements(event)

    def loadSubElements(self, event):
        #Place les éléments constituant la boîte dans celle-ci
        elements = []


        #Nom de l'évènement
        #Description
        #Ressources utilisées
        #Utilisateurs inscrits
        elements.append(EventTypeLabel(event.type))
        elements.append(EventDescriptionScrollable(event.description))
        elements.append(EventResourcesScrollable(event.resources))
        elements.append(EventUsersScrollable(event.users))
        
        for el in elements:
            self.add(el)
            
class EventTypeLabel(Gtk.Label):
    #Label d'affichage du type d'un évènement
    def __init__(self, eventType):
        Gtk.Label.__init__(self)
        self.set_text(eventType)

class EventDescriptionScrollable(Gtk.ScrolledWindow):
    #Fenêtre défilable, contient la description d'un évènement
    def __init__(self, description):
        Gtk.ScrolledWindow.__init__(self)  
        label = Gtk.Label()
        label.set_line_wrap(True)
        label.set_text(description)
        self.set_property("expand",True)
        self.add(label)

class EventResourcesScrollable(Gtk.ScrolledWindow):
    #Fenêtre défilable, contient les ressources d'un évènement
    def __init__(self, resources):
        Gtk.ScrolledWindow.__init__(self)
        resourcesFlowBox = Gtk.FlowBox(orientation = Gtk.Orientation.HORIZONTAL)
        resourcesFlowBox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.add(resourcesFlowBox)
        for resource in resources:
            resourcesFlowBox.add(EventResourceBox(resource))
   
class EventResourceBox(Gtk.Box):
    #Boîte d'affichage d'une ressource
    def __init__(self, resource):
        Gtk.Box.__init__(self)

        frame = Gtk.Frame()
        subBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 5)
        
        subBox.add(Gtk.Label(label = "{} ({})".format(resource.name,resource.capacity)))
        subBox.add(Gtk.Label(label = resource.location))

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

class EventUserBox(Gtk.Box):
    #Boîte d'affichage d'un utilisateur
    def __init__(self, user):
        Gtk.Box.__init__(self)
        frame = Gtk.Frame()
        frame.add(Gtk.Label(label="{} {}".format(user.first_name, user.last_name)))
        self.add(frame)
