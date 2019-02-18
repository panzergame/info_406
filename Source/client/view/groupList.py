import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .group import *
from client.model import common

#######################################################################################################################

# Classe définissant une liste de groupes :

class GroupList(Gtk.Box):
    # On appelle le constructeur de la classe mère avec un agencement vertical et un espacement entre éléments
    # de 6 pixels :
    def __init__(self, common):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing = 6)
        # Actions sur les attributs :

        # On donne un titre à notre boîte :
        self.title = Gtk.Label("\tGroupes : ", xalign=0)

        # On donne une liste en attribut :
        self.groupList = Gtk.ListBox()

        # On donne l'user courant en attribut :
        self.user = common.user_clicked

        # On ajoute ce titre à notre boîte :
        self.pack_start(self.title, False, True, 0)

        # On ajoute cette liste à notre boîte :
        self.pack_start(self.groupList, True, True, 0)

        # On appelle l'affichage des infos utilisateur :
        self.getUserData(self.user)

    # Méthodes :

    # On definie la méthode permettant d'ajouter un groupe à notre boîte :
    def addGroup(self, name):
        group = Group(name)
        self.groupList.add(group)

    def getUserData(self, user):
        # On recupère les groupes liés à l'utilisateur
        groups = user.groups
        # On ajoute tous les groupes de l'utilisateur à notre liste :
        for group in groups:
            g = Group(group.name)
            self.groupList.add(g)
            agendas = group.agendas
            # On ajoute tous les agendas lié au groupe courant dans la liste des agendas du groupe :
            for agenda in agendas:
               # a = Agenda(agenda.name)
                g.addAgenda(agenda.name)
        # Affichage des groupes de l'utilisateur sélectionné (courant) :
