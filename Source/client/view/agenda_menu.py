# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .user_filter import *
from .resource_filter import *
from .add_event import *
from .agenda_calendar import *

class AgendaMenu(Gtk.HBox):
	def __init__(self, common):
		Gtk.HBox.__init__(self)

		self.add(UserFilter(common))
		self.add(ResourceFilter(common))
		self.add(AddEventButton(common))
		self.add(AgendaCalendar(common))
