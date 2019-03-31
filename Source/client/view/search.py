# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *

from .group import *

class SearchBox(Gtk.VBox):
	def __init__(self, common):
		super().__init__()
		self.common = common

		#"Rechercher un groupe"
		self.entry = Gtk.SearchEntry()
		self.entry.connect("search-changed", self.on_search_changed)

		self.list = GroupList(self.common)

		self.add(self.entry)
		self.add(self.list)

	def on_search_changed(self, widget):
		sub = self.entry.get_text()
		groups = self.common.collection.load_groups(sub)

		self.list.set_groups(groups)
