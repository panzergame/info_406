# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *

from .group_list import *

class SearchBox(Gtk.VBox, ViewObserver):
	def __init__(self, common):
		Gtk.VBox.__init__(self)
		ViewObserver.__init__(self, common, common.user_clicked, common.group_clicked)

		#"Rechercher un groupe"
		self.entry = Gtk.SearchEntry()
		self.entry.connect("search-changed", self.on_search_changed)
		self.sub = self.entry.get_text()

		self.list = GroupList(self.common)

		recherche = Gtk.Label()
		recherche.set_markup("\n <big> Rechercher un groupe </big> \n")
		self.pack_start(recherche, False , False ,False)
		self.pack_start(self.entry, False, False, False)
		self.add(self.list)

	def on_search_changed(self, widget):
		self.sub = self.entry.get_text()
		self.update()

	def update(self):
		groups = self.common.collection.load_groups(self.sub)
		self.list.set_groups(groups)
