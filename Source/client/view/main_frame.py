# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .main_box import *

class MainFrame(Gtk.Window):
    def __init__(self, common):
        Gtk.Window.__init__(self, title="Votre Agenda")
        self.add(MainBox(common))
