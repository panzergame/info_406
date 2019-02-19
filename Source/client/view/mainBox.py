# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .left import LeftBox
from .right import RightBox
from .centerBox import *
from .agenda import *
from client.model import common


class MainBox(Gtk.Box):
    """Boîte contenant tout ce qui est affiché à l'écran"""
    def __init__(self, common):
        self.common = common

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.set_border_width(10)

        grid = Gtk.Grid()
        grid.attach(LeftBox(self.common), 0, 0, 1, 1)
        grid.attach(CenterBox(self.common), 1, 0, 6, 1)
        grid.attach(RightBox(self.common), 7, 0, 1, 1)

        self.add(grid)
        self.show_all()
