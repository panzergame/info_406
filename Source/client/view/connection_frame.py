# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from core import *
from .connection_box import *
from .registration_box import *


class ConnectionWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Se connecter")
		self.add(ConnectionBox())
		self.set_resizable(False)
