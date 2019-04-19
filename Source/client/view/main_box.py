# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .left import LeftBox
from .right import RightBox
from .center import CenterBox
from .menu_bar import MenuBar
from .agenda import AgendaBox

class MainBox(Gtk.Box):
    """Boîte contenant tout ce qui est affiché à l'écran"""
    def __init__(self, common):
        self.common = common

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.set_border_width(10)
        menu = MenuBar(self.common)

        grid = Gtk.Grid()
        grid.attach(menu, 0, 0, 8, 1)
        grid.attach(LeftBox(self.common), 0, 1, 1, 1)
        grid.attach(CenterBox(self.common), 1, 1, 6, 1)
        grid.attach(RightBox(self.common), 7, 1, 1, 1)

        self.add(grid)
        self.show_all()

