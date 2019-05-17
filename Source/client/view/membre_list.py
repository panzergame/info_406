# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

from .observer import *

class MembreList(Gtk.VBox, ViewObserver):
	def __init__(self, common):
		Gtk.VBox.__init__(self)
		ViewObserver.__init__(self, common, common.group_clicked)

		self.list = Gtk.ListStore(str, str, object)

		self.view = Gtk.TreeView(self.list)

		render_fname = Gtk.CellRendererText()
		fname_column = Gtk.TreeViewColumn("Prénom", render_fname, text=0)

		render_lname = Gtk.CellRendererText()
		lname_column = Gtk.TreeViewColumn("Nom", render_lname, text=1)

		self.view.append_column(fname_column)
		self.view.append_column(lname_column)

		self.update()

		membrel = Gtk.Label()

		membrel.set_markup("\n \n <big> Membres du groupe </big> \n")

		self.pack_start(membrel, False, False, 0)
		self.add(self.view)

	def update(self):
		self.list.clear()

		group = self.common.group_clicked.value

		if group is not None:
			for user in group.subscribers:
				self.list.append((user.first_name, user.last_name, user))
