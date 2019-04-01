# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *

class GroupList(Gtk.VBox):
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

		view.connect("row-activated", self.on_agenda_changed)

		self.add(view)

	def on_toggled(self, widget, path):
		name, current_value, item = self.tree[path]
		user = self.common.user_clicked

		if len(path) == 1:
			if not current_value:
				item.subscribe(user)
			else:
				item.unsubscribe(user)
			self.tree[path][1] = not self.tree[path][1]

		elif len(path) == 3:
			if item.group in user.groups:
				agenda = user.agenda
				if item in agenda.linked_agendas:
					agenda.unlink_agenda(item)
				else:
					agenda.link_agenda(item)

				print(agenda.linked_agendas)
				self.common._notify()

				self.tree[path][1] = not self.tree[path][1]

		self.common._notify()

	def on_agenda_changed(self, model, path, column):
		item = self.tree[path][2]
		if isinstance(item, Group):
			self.common.group_clicked = item
		elif isinstance(item, Agenda):
			self.common.agenda_displayed = item

	def set_groups(self, groups):
		self.tree.clear()

		for group in groups:
			iter = self.tree.append(None, (group.name, (group in self.common.user_clicked.groups), group))
			for agenda in group.agendas:
				self.tree.append(iter, (agenda.name, (agenda in self.common.agenda_displayed.linked_agendas), agenda))
