# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from client.model import common
from .agenda_title import AgendaTitleBox
from .agenda import AgendaBox
from .add_event import AddEventButton
from .link_button import LinkButton

class CenterBox(Gtk.Box):
	"""Boîte contenant tout ce qui est affiché à l'écran"""
	def __init__(self, common):
		self.common = common

		Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(AgendaTitleBox(self.common))
		self.add(AgendaBox(self.common))
		self.add(AddEventButton(self.common))

		self.show_all()
