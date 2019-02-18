import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from group import *

#######################################################################################################################

# Classe définissant une liste de groupes :

class GroupList(Gtk.Box):
    # On appelle le constructeur de la classe mère avec un agencement vertical et un espacement entre éléments
    # de 6 pixels :
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing = 6)
        # Actions sur les attributs :

        # On donne un titre à notre boîte :
        self.title = Gtk.Label("\tGroupes : ", xalign=0)

        # On donne une liste en attribut :
        self.groupList = Gtk.ListBox()

        # On ajoute ce titre à notre boîte :
        self.pack_start(self.title, False, True, 0)

        # On ajoute cette liste à notre boîte :
        self.pack_start(self.groupList, True, True, 0)

    # Méthodes :

    # On definie la méthode permettant d'ajouter un groupe à notre boîte :
    def addGroup(self, name):
        group = Group(name)
        self.groupList.add(group)