# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .user_page import *
from .group_page import *
from .friend_page import *

class LeftBox(Gtk.VBox, ViewObserver):
	"""Partie gauche de l'écran , avec les deu onglets groupe et utilisateur et liste d'amis"""

	def __init__(self, common):
		Gtk.VBox.__init__(self)
		ViewObserver.__init__(self, common, common.group_clicked)

		self.group_label = Gtk.Label('Groupe')

		user = UserPage(common)
		groups = GroupPage(common)
		friend = FriendPage(common)

		notebook = Gtk.Notebook()
		notebook.append_page(user, Gtk.Label('Votre Agenda'))
		notebook.append_page(groups, self.group_label)
		notebook.append_page(friend , Gtk.Label('Vos Contacts'))

		self.add(notebook)

	def update(self):
		group = self.common.group_clicked.value

		if group is not None:
			self.group_label.set_text(group.name)
		else:
			self.group_label.set_text("Groupe")
