# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from client.model import common
from .agenda_title import AgendaTitleBox
from .agenda import AgendaBox
from .agenda_menu import *

class CenterBox(Gtk.VBox):
	"""Boîte contenant tout ce qui est affiché à l'écran"""
	def __init__(self, common):
		super().__init__()

		self.pack_start(AgendaTitleBox(common), False, False, 0)
		self.add(AgendaBox(common))
		self.pack_end(AgendaMenu(common), False, False, 0)
