import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .agenda import *

# Classe definissant un groupe :

class Group(Gtk.ListBoxRow):
    # On appelle le constructeur de la classe mère :
    def __init__(self, name):
        Gtk.ListBoxRow.__init__(self)

        # Actions sur les attributs :

        # On donne une boite horizontale en attribut :
        self.groupLine = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing = 6)

        # On crée un bouton de couleur (qui sera associée au groupe) :
        self.color = Gtk.ColorButton()

        # On crée un label avec le nom de notre groupe :
        self.name = Gtk.Label(name, xalign=0)

        # On crée la liste d'agendas liée à notre ligne (groupe) :
        self.agendasList = Gtk.ListBox()

        # On ajoute la couleur, le nom et la liste d'agendas à notre groupe (groupLine) :
        self.groupLine.pack_start(self.color, False, True, 0)
        self.groupLine.pack_start(self.name, False, True, 0)
        self.groupLine.pack_start(self.agendasList, False, True, 0)

        # On ajoute notre boite groupLine à notre ligne (Group) qui contiendra les agendas de son groupe associé :
        self.add(self.groupLine)

    # Méthodes :

    # On definie la méthode nous permettant d'ajouter un agenda :
    def addAgenda(self, name):
        agenda = Agenda(name)
        self.agendasList.add(agenda)
