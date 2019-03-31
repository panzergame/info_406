# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *

class SearchBox(Gtk.VBox):
	def __init__(self, common):
		super().__init__()
		self.common = common

		self.tree = Gtk.TreeStore(str, bool, object)

		view = Gtk.TreeView(self.tree)
		render_agenda = Gtk.CellRendererText()
		agenda_column = Gtk.TreeViewColumn("", render_agenda, text=0)

		render_subscribe = Gtk.CellRendererToggle()
		subscribe_column = Gtk.TreeViewColumn("S'inscrire", render_subscribe, active=1)

		render_subscribe.connect("toggled", self.on_toggled)

		view.append_column(agenda_column)
		view.append_column(subscribe_column)

		select = view.get_selection()
		select.connect("changed", self.on_agenda_changed)

		#"Rechercher un groupe"
		self.entry = Gtk.SearchEntry()
		self.entry.connect("search-changed", self.on_search_changed)

		self.add(self.entry)
		self.add(view)

	def on_toggled(self, widget, path):
		name, current_value, item = self.tree[path]
		if len(path) == 1:
			if not current_value:
				item.subscribe(self.common.user_clicked)
			else:
				item.unsubscribe(self.common.user_clicked)

			self.tree[path][1] = not self.tree[path][1]


	def on_agenda_changed(self, selection):
		model, iter = selection.get_selected()
		if iter is not None:
			item = model[iter][2]
			if isinstance(item, Group):
				self.common.group_clicked = item
			elif isinstance(item, Agenda):
				self.common.agenda_displayed = item

	def on_search_changed(self, widget):
		self.tree.clear()
		sub = self.entry.get_text()
		groups = self.common.collection.load_groups(sub)

		for group in groups:
			iter = self.tree.append(None, (group.name, (group in self.common.user_clicked.groups), group))
			for agenda in group.agendas:
				self.tree.append(iter, (agenda.name, (agenda in self.common.agenda_displayed.linked_agendas), agenda))
