# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import re

from .observer import *

class UserFilter(Gtk.VBox, ViewObserver):
	def __init__(self, common):
		Gtk.VBox.__init__(self)
		ViewObserver.__init__(self, common, common.group_clicked)

		self.list = Gtk.ListStore(str, str, bool, object)
		self.filter = self.list.filter_new()
		self.view = Gtk.TreeView(self.list)

		first_name = Gtk.CellRendererText()
		last_name = Gtk.CellRendererText()

		name_column = Gtk.TreeViewColumn("Nom")
		name_column.pack_start(first_name, True)
		name_column.pack_start(last_name, True)
		name_column.add_attribute(first_name, "text", 0)
		name_column.add_attribute(last_name, "text", 1)

		selected = Gtk.CellRendererToggle()
		selected.connect("toggled", self.on_selected)
		select_column = Gtk.TreeViewColumn("Sélectionné(s)", selected, active=2)

		self.view.append_column(name_column)
		self.view.append_column(select_column)

		self.popover = Gtk.Popover()
		self.popover.add(self.view)
		self.popover.set_position(Gtk.PositionType.BOTTOM)

		self.button = Gtk.Button("Participants")
		self.button.connect("clicked", self.on_clicked)

		self.add(self.button)

		self.update()

	def on_clicked(self, button):
		self.popover.set_relative_to(self.button)
		self.popover.show_all()
		self.popover.popup()

	def on_selected(self, widget, path):
		row = self.list[path]
		row[2] = not row[2]

		user = row[3]
		group = self.common.group_clicked.value

		if group not in self.common.users_filtered.value:
			users = self.common.users_filtered.value[group] = set()
		else:
			users = self.common.users_filtered.value[group]

		if row[2]:
			users.add(user)
		else:
			users.discard(user)

		self.common.users_filtered.notify()

	def update(self):
		group = self.common.group_clicked.value

		self.list.clear()

		if group is not None:
			for user in group.subscribers:
				self.list.append((user.first_name, user.last_name, False, user))
