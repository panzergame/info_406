# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .user_switch import *
from .disconnect import *
from .synchronize import *

class HeaderBox(Gtk.HBox):
	def __init__(self, common):
		Gtk.HBox.__init__(self)

		self.common = common

		disconnect = Disconnect(common)
		user_switch = UserSwitch(common)
		sync = Synchronize(common)

		self.pack_start(disconnect, False, False, 0)
		self.pack_start(user_switch, False, False, 0)
		self.pack_start(sync, False, False, 0)
