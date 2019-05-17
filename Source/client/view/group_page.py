# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

from .membre_list import *
from .agenda_list import *
from .resource_list import *
from .add_group import *
from .search import *
from .observer import *

class GroupPage(Gtk.ScrolledWindow, ViewObserver):
	def __init__(self, common):
		Gtk.ScrolledWindow.__init__(self)
		ViewObserver.__init__(self, common, common.group_clicked)

		box = Gtk.VBox()

		self.members = MembreList(common)
		self.agendas = AgendaList(common)
		self.resources = ResourceList(common)
		self.add_group = AddGroupButton(common)
		self.search = SearchBox(common)

		box.pack_start(self.search, False, False, False)
		box.pack_start(self.add_group, False, False, False)
		box.add(self.members)
		box.add(self.agendas)
		box.add(self.resources)

		self.add(box)

	def update(self):
		group = self.common.group_clicked.value

		if group is not None:
			self.members.show()
			self.agendas.show()
			self.resources.show()
		else:
			self.members.hide()
			self.agendas.hide()
			self.resources.hide()
