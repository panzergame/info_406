# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

from .observer import *

class ResourceList(Gtk.VBox, ViewObserver):
	def __init__(self, common):
		Gtk.VBox.__init__(self)
		ViewObserver.__init__(self, common, common.group_clicked)

		self.list = Gtk.ListStore(str, str, int, object)

		self.view = Gtk.TreeView(self.list)

		render_name = Gtk.CellRendererText()
		name_column = Gtk.TreeViewColumn("Nom", render_name, text=0)

		render_loc = Gtk.CellRendererText()
		loc_column = Gtk.TreeViewColumn("Location", render_loc, text=1)

		render_cap = Gtk.CellRendererText()
		cap_column = Gtk.TreeViewColumn("Capacité", render_cap, text=2)


		self.view.append_column(name_column)
		self.view.append_column(loc_column)
		self.view.append_column(cap_column)

		self.update()

		self.add(Gtk.Label("Ressources du groupe"))
		self.add(self.view)

	def update(self):
		self.list.clear()

		group = self.common.group_clicked.value

		if group is not None:
			for res in group.resources:
				self.list.append((res.name, res.location, res.capacity, res))
