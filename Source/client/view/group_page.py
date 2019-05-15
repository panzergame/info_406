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

class GroupPage(Gtk.VBox, ViewObserver):
	def __init__(self, common):
		Gtk.VBox.__init__(self)
		ViewObserver.__init__(self, common, common.group_clicked)

		self.members = MembreList(common)
		self.agendas = AgendaList(common)
		self.resources = ResourceList(common)
		self.add_group = AddGroupButton(common)
		self.search = SearchBox(common)

		self.pack_start(self.search, False, False, False)
		self.pack_start(self.add_group, False, False, False)
		self.add(self.members)
		self.add(self.agendas)
		self.add(self.resources)

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
