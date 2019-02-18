import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from search import SearchBox
from account import AccountBox
from group import *
from Source.client.model import common


class LeftBox(Gtk.Box):
    """Partie Gauche de l'écran, avec les utilisateurs, les groupes (en attente de Xavier), et la zeone de recherche"""
    def __init__(self, account, common):
        self.account = account
        self.common = common

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_border_width(10)

        self.add(AccountBox(self.account, self.common))
        self.add(SearchBox())

        # Creation de la boîte groupes :
        self.groupList = GroupList()

        # Ajout des groupes de l'utilisateur sélectionné (courant) a la liste :
        user = self.common.user_clicked
        groups = user.groups

        # On ajoute tous les groupes de l'utilisateur à notre liste :
        for group in groups:
            g = Group(group.name)
            self.GroupList.groupList.add(g)
            agendas = group.agendas
            # On ajoute tous les agendas lié au groupe courant dans la liste des agendas du groupe :
            for agenda in agendas:
                a = Agenda(agenda.name, agenda.owner)
                g.addAgenda(a)
        # Affichage des groupes de l'utilisateur sélectionné (courant) :