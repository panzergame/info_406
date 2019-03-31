# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class SearchBox(Gtk.Box):
	def __init__(self, common):
		super().__init__()

		self.common = common

		#"Rechercher un groupe"
		self.entry = Gtk.SearchEntry()
		self.entry.connect("search-changed", self.on_search_changed)

		self.add(self.entry)

	def on_search_changed(self, widget):
		print(self.entry.get_text())
