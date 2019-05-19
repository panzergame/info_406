# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Synchronize(Gtk.Button):
	def __init__(self, common):
		Gtk.Button.__init__(self, "Enregistrer")

		self.common = common

		self.connect("clicked", self.on_clicked)

	def on_clicked(self, button):
		self.common.collection.flush()
