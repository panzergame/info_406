# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import re

from .observer import *

class ResourceFilter(Gtk.VBox, ViewObserver):
	def __init__(self, common):
		Gtk.VBox.__init__(self)
		ViewObserver.__init__(self, common, common.group_clicked)

		self.list = Gtk.ListStore(str, str, int, bool, object)
		self.filter = self.list.filter_new()
		self.view = Gtk.TreeView(self.list)

		render_name = Gtk.CellRendererText()
		name_column = Gtk.TreeViewColumn("Nom", render_name, text=0)

		render_loc = Gtk.CellRendererText()
		loc_column = Gtk.TreeViewColumn("Location", render_loc, text=1)

		render_cap = Gtk.CellRendererText()
		cap_column = Gtk.TreeViewColumn("Capacité", render_cap, text=2)

		selected = Gtk.CellRendererToggle()
		selected.connect("toggled", self.on_selected)
		select_column = Gtk.TreeViewColumn("Sélectionné(s)", selected, active=3)

		self.view.append_column(name_column)
		self.view.append_column(loc_column)
		self.view.append_column(cap_column)
		self.view.append_column(select_column)

		self.popover = Gtk.Popover()
		self.popover.add(self.view)
		self.popover.set_position(Gtk.PositionType.BOTTOM)

		self.button = Gtk.Button("Ressources")
		self.button.connect("clicked", self.on_clicked)

		self.add(self.button)

		self.update()

	def on_clicked(self, button):
		self.popover.set_relative_to(self.button)
		self.popover.show_all()
		self.popover.popup()

	def on_selected(self, widget, path):
		row = self.list[path]
		row[3] = not row[3]

		res = row[4]
		group = self.common.group_clicked.value

		if group not in self.common.resources_filtered.value:
			resources = self.common.resources_filtered.value[group] = set()
		else:
			resources = self.common.resources_filtered.value[group]

		if row[2]:
			resources.add(res)
		else:
			resources.discard(res)

		self.common.resources_filtered.notify()

	def update(self):
		group = self.common.group_clicked.value

		self.list.clear()

		if group is not None:
			for res in group.resources:
				self.list.append((res.name, res.location, res.capacity, False, res))
