# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from client.model import common
from .agenda_title import AgendaTitleBox
from .agenda import AgendaBox
from .add_event import AddEventButton
from .link_button import LinkButton

class CenterBox(Gtk.VBox):
	"""Boîte contenant tout ce qui est affiché à l'écran"""
	def __init__(self, common):
		super().__init__()

		self.pack_start(AgendaTitleBox(common), False, False, False)
		self.add(AgendaBox(common))
		self.pack_end(AddEventButton(common), False, False, False)
