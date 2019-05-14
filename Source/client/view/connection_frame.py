# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from core import *
from .connection_box import *
from .registration_box import *


class ConnectionWindow(Gtk.Window, ViewObserver):
	def __init__(self, common):
		Gtk.Window.__init__(self, title="Se connecter")
		ViewObserver.__init__(self, common)

		self.box = self.choose_box()
		self.add(self.box)

		self.set_resizable(False)

	def choose_box(self):
		if self.common.has_account.value:
			box = ConnectionBox(self.common)
		else:
			box = RegistrationBox(self.common)
		return box

	"""def update(self, common):
		self.remove(self.box)
		self.common = common
		self.box = self.choose_box()
		self.add(self.box)
		self.box.show_all()""" # TODO ??
