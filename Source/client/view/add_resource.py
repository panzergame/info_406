# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from core import *

class AddResourceDialog(Gtk.Dialog):
	def __init__(self):
		Gtk.Dialog.__init__(self, "Ajouter une ressource", None, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OK, Gtk.ResponseType.OK))

		self.name_entry = Gtk.Entry()
		self.name_entry.set_text("nom")

		self.location_entry = Gtk.Entry()
		self.location_entry.set_text("location")

		self.capacity_entry = Gtk.Entry()
		self.capacity_entry.set_text("0")

		box = self.get_content_area()
		box.add(self.name_entry)
		box.add(self.location_entry)
		box.add(self.capacity_entry)

		self.show_all()

	@property
	def name(self):
		return self.name_entry.get_text()

	@property
	def location(self):
		return self.location_entry.get_text()

	@property
	def capacity(self):
		try:
			value = int(self.capacity_entry.get_text())
		except:
			value = 0

		return value

class AddResourceButton(Gtk.Button):
	def __init__(self, common):
		super().__init__("Ajouter une ressource")
		self.connect("clicked", self.on_clicked)

		self.common = common

	def on_clicked(self, button):
		group = self.common.group_clicked.value
		if group is not None:
			dia = AddResourceDialog()

			if dia.run() == Gtk.ResponseType.OK:
				res = Resource.new(self.common.collection, dia.name, dia.location, dia.capacity)
				group.add_resource(res)
				self.common.group_clicked.notify()

			dia.destroy()
