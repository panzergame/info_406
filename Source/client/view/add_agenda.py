# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from core import *

class AddAgendaDialog(Gtk.Dialog):
	def __init__(self):
		Gtk.Dialog.__init__(self, "Ajouter un agenda", None, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OK, Gtk.ResponseType.OK))

		self.name_entry = Gtk.Entry()
		self.name_entry.set_text("nom")

		box = self.get_content_area()
		box.add(self.name_entry)

		self.show_all()

	@property
	def name(self):
		return self.name_entry.get_text()

class AddAgendaButton(Gtk.Button):
	def __init__(self, common):
		super().__init__("Ajouter un agenda")
		self.connect("clicked", self.on_clicked)

		self.common = common

	def on_clicked(self, button):
		group = self.common.group_clicked.value
		if group is not None:
			dia = AddAgendaDialog()

			if dia.run() == Gtk.ResponseType.OK:
				ag = Agenda.new(self.common.collection, dia.name)
				group.add_agenda(ag)
				self.common.group_clicked.notify()

			dia.destroy()
