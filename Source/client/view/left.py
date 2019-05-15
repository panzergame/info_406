# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .user_page import *
from .user_switch import *
from .disconnect import *
from .group_page import *

class LeftBox(Gtk.VBox, ViewObserver):
	"""Partie gauche de l'écran , avec les deu onglets groupe et utilisateur"""
	
	def __init__(self, common):
		Gtk.VBox.__init__(self)
		ViewObserver.__init__(self, common, common.group_clicked)

		self.group_label = Gtk.Label('Groupe')

		disconnect = Disconnect(common)
		user_switch = UserSwitch(common)
		user = UserPage(common)
		groups = GroupPage(common)

		header = Gtk.VBox()
		header.add(user_switch)
		header.add(disconnect)

		notebook = Gtk.Notebook()
		notebook.append_page(user, Gtk.Label('Votre Agenda'))
		notebook.append_page(groups, self.group_label)

		self.pack_start(header, False, False, False)
		self.add(notebook)

	def update(self):
		group = self.common.group_clicked.value

		if group is not None:
			self.group_label.set_text(group.name)
		else:
			self.group_label.set_text("Groupe")
