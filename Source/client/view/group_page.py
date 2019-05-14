# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

from .membre_list import *
from .agenda_list import *
from .resource_list import *
from .add_group import *
from .search import *

class GroupPage(Gtk.VBox):
	def __init__(self, common):
		super().__init__()

		
		members = MembreList(common)
		agendas = AgendaList(common)
		resources = ResourceList(common)
		add_group = AddGroupButton(common)
		search = SearchBox(common)

		self.pack_start(search, False, False, False)
		self.pack_start(add_group, False, False, False)
		self.add(members)
		self.add(agendas)
		self.add(resources)
