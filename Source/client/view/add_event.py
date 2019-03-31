# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .date_time import DateTimeDialog
from core import *
from datetime import datetime

def datetime_str(date):
	return date.strftime("%d/%m/%Y à %H:%M")

class AddEventDialog(Gtk.Dialog):
	def __init__(self, parent):
		Gtk.Dialog.__init__(self, "Ajouter un événement", parent, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OK, Gtk.ResponseType.OK))

		self.start = datetime.now()
		self.end = datetime.now()

		self.name_entry = Gtk.Entry()
		self.name_entry.set_text("nom")

		self.type_entry = Gtk.Entry()
		self.type_entry.set_text("type")

		self.description_entry = Gtk.Entry()
		self.description_entry.set_text("description")

		self.start_button = Gtk.Button(datetime_str(self.start))
		self.start_button.connect("clicked", self.on_start_clicked)

		self.end_button = Gtk.Button(datetime_str(self.end))
		self.end_button.connect("clicked", self.on_end_clicked)

		box = self.get_content_area()
		box.add(self.name_entry)
		#box.add(self.type_entry)
		box.add(self.description_entry)

		row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		row.pack_start(self.start_button, True, True, 0)
		row.pack_start(Gtk.Label("jusqu'à"), True, True, 0)
		row.pack_start(self.end_button, True, True, 0)

		box.pack_start(row, True, True, 0)

		self.show_all()

	def on_start_clicked(self, button):
		date = DateTimeDialog(self)

		if date.run() == Gtk.ResponseType.OK:
			self.start = datetime(date.year, date.month, date.day, date.hour, date.minute)
			self.start_button.set_label(datetime_str(self.start))

		date.destroy()

	def on_end_clicked(self, button):
		date = DateTimeDialog(self)

		if date.run() == Gtk.ResponseType.OK:
			self.end = datetime(date.year, date.month, date.day, date.hour, date.minute)
			self.end_button.set_label(datetime_str(self.end))

		date.destroy()

	@property
	def name(self):
		return self.name_entry.get_text()

	@property
	def type(self):
		return self.type_entry.get_text()

	@property
	def description(self):
		return self.description_entry.get_text()

class AddEventButton(Gtk.Button):
	def __init__(self, parent, common):
		Gtk.Button.__init__(self, "Ajouter")
		self.connect("clicked", self.on_clicked)

		self.common = common
		self.parent = parent

	def on_clicked(self, button):
		dia = AddEventDialog(self.parent)

		if dia.run() == Gtk.ResponseType.OK:
			agenda = self.common.user_clicked.agenda
			event = Event.new(agenda.collection, dia.start, dia.end, dia.name, dia.description, set(), set())
			agenda.add_event(event)
			self.common.event_clicked = event
		dia.destroy()
