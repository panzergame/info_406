# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .observer import *

class UserSwitch(Gtk.HBox, ViewObserver):
	def __init__(self, common):
		Gtk.HBox.__init__(self)
		ViewObserver.__init__(self, common, common.account)

		self.list = Gtk.ListStore(str, object)

		combo = Gtk.ComboBox.new_with_model(self.list)
		combo.connect("changed", self.on_combo_changed)

		renderer_text = Gtk.CellRendererText()
		combo.pack_start(renderer_text, True)
		combo.add_attribute(renderer_text, "text", 0)

		self.pack_start(Gtk.Label("Choisir un utilisateur :"), False, False, False)
		self.add(combo)

		self.update()

	def on_combo_changed(self, combo):
		tree_iter = combo.get_active_iter()
		if tree_iter is not None:
			user = self.list[tree_iter][1]

			self.common.user_clicked.value = user
			self.common.agenda_displayed.value = user.agenda

	def update(self):
		self.list.clear()

		account = self.common.account.value

		if account is not None:
			for user in account.users:
				self.list.append((user.first_name + " " + user.last_name, user))
