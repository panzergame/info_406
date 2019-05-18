# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .left import LeftBox
from .right import RightBox
from .center import CenterBox
from .header import *

class MainBox(Gtk.HBox):
    """Boîte contenant tout ce qui est affiché à l'écran"""
    def __init__(self, common):
        super().__init__()

        grid = Gtk.Grid()
        grid.attach(HeaderBox(common), 0 , 0, 7 ,1)
        grid.attach(LeftBox(common), 0, 1, 1, 1)
        grid.attach(CenterBox(common), 1, 1, 6, 1)
        grid.attach(RightBox(common), 7, 1, 1, 1)

        self.add(grid)
