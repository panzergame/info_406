# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .left import LeftBox
from client.model import common


class MainBox(Gtk.Box):
    """Boîte contenant tout ce qui est affiché à l'écran"""
    def __init__(self, account, common):
        self.account = account
        self.common = common

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.set_border_width(10)

        self.add(LeftBox(self.account, self.common))
