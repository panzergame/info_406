# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from core import *

class AddGroupDialog(Gtk.Dialog):
	def __init__(self):
		Gtk.Dialog.__init__(self, "Ajouter un groupe", None, 0,
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


class AddGroupButton(Gtk.Button):
	def __init__(self, common):
		Gtk.Button.__init__(self)
		add_img = Gtk.Image()
		add_img.set_from_file("client/view/image/add.png")
		self.add(add_img)
		self.connect("clicked", self.on_clicked)

		self.common = common

	def on_clicked(self, button):
		dia = AddGroupDialog()

		if dia.run() == Gtk.ResponseType.OK:
			group = Group.new(self.common.collection, dia.name, set(), set(), set(), set())
			self.common.group_clicked.value = group

		dia.destroy()
