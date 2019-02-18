# -*- coding: utf-8 -*-

import gi


gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .search import SearchBox
from .account import AccountBox
from .groupList import *
from client.model import common


class LeftBox(Gtk.Box):
    """Partie Gauche de l'écran, avec les utilisateurs, les groupes (en attente de Xavier), et la zeone de recherche"""
    def __init__(self, account, common):
        self.account = account
        self.common = common

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_border_width(10)

        self.add(AccountBox(self.account, self.common))
        self.add(GroupList(self.common))
        self.add(SearchBox())

