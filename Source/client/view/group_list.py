# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *
from .observer import *

class GroupList(Gtk.VBox, ViewObserver):
	def __init__(self, common):
		Gtk.VBox.__init__(self)
		ViewObserver.__init__(self, common)

		self.tree = Gtk.TreeStore(str, bool, object)

		self.view = Gtk.TreeView(self.tree)
		render_agenda = Gtk.CellRendererText()
		agenda_column = Gtk.TreeViewColumn("", render_agenda, text=0)

		render_subscribe = Gtk.CellRendererToggle()
		subscribe_column = Gtk.TreeViewColumn("S'inscrire", render_subscribe, active=1)

		render_subscribe.connect("toggled", self.on_toggled)

		self.view.append_column(agenda_column)
		self.view.append_column(subscribe_column)

		self.view.connect("row-activated", self.on_agenda_changed)

		self.add(self.view)

	def on_toggled(self, widget, path):
		name, current_value, item = self.tree[path]
		user = self.common.user_clicked.value

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

				#self.common._notify() TODO

				self.tree[path][1] = not self.tree[path][1]

		#self.common._notify() TODO

	def on_agenda_changed(self, model, path, column):
		item = self.tree[path][2]
		if isinstance(item, Group):
			self.common.group_clicked.value = item
		elif isinstance(item, Agenda):
			self.common.agenda_displayed.value = item

	def set_groups(self, groups):
		self.tree.clear()

		for group in groups:
			iter = self.tree.append(None, (group.name, (group in self.common.user_clicked.value.groups), group))
			for agenda in group.agendas:
				self.tree.append(iter, (agenda.name, (agenda in self.common.agenda_displayed.value.linked_agendas), agenda))

		self.view.expand_all()

