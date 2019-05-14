# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

from .observer import *

class AgendaList(Gtk.VBox, ViewObserver):
	def __init__(self, common):
		Gtk.VBox.__init__(self)
		ViewObserver.__init__(self, common, common.group_clicked)

		self.list = Gtk.ListStore(str, object)

		self.view = Gtk.TreeView(self.list)

		render_name = Gtk.CellRendererText()
		name_column = Gtk.TreeViewColumn("Nom", render_name, text=0)

		self.view.append_column(name_column)

		self.view.connect("row-activated", self.on_agenda_changed)

		self.update()

		self.add(Gtk.Label("Agenda du groupe"))
		self.add(self.view)

	def on_agenda_changed(self, model, path, column):
		item = self.list[path][1]
		self.common.agenda_displayed.value = item

	def update(self):
		self.list.clear()

		group = self.common.group_clicked.value

		if group is not None:
			for agenda in group.agendas:
				self.list.append((agenda.name, agenda))
