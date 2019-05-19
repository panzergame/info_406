# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .date_time import DateTimeDialog
from .user_filter import *
from .resource_filter import *
from core import *
from datetime import datetime
from datetime import timedelta
from .conflict_dialogs import *

def datetime_str(date):
	return date.strftime("%d/%m/%Y à %H:%M")

class AddEventDialog(Gtk.Dialog):
	def __init__(self, common, ex_event = None):
		if ex_event is None:
			title = "Ajouter un événement"
		else:
			title = "Modifier un événement"

		Gtk.Dialog.__init__(self, title , None, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OK, Gtk.ResponseType.OK))
		self.common = common

		self.name_entry = Gtk.Entry()
		self.type_entry = Gtk.Entry()
		self.description_entry = Gtk.Entry()

		if ex_event is None:
			self.start = datetime.now().replace(minute=0)
			self.end = self.start + timedelta(minutes=30)
			self.name_entry.set_text("nom")
			self.type_entry.set_text("type")
			self.description_entry.set_text("description")

		else:
			self.start = ex_event.start
			self.end = ex_event.end
			self.name_entry.set_text(ex_event.type)
			self.type_entry.set_text("type") #TODO quand type sera mis, il faudra que ça prenne la bonne valeur
			self.description_entry.set_text(ex_event.description)


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
		date = DateTimeDialog(self, self.start)

		if date.run() == Gtk.ResponseType.OK:
			self.start = datetime(date.year, date.month, date.day, date.hour, date.minute)
			self.start_button.set_label(datetime_str(self.start))

			if (self.start >= self.end):
				self.end = self.start + timedelta(minutes = 30)
				self.end_button.set_label(datetime_str(self.end))

		date.destroy()

	def on_end_clicked(self, button):
		date = DateTimeDialog(self, self.end)

		if date.run() == Gtk.ResponseType.OK:
			self.end = datetime(date.year, date.month, date.day, date.hour, date.minute)
			self.end_button.set_label(datetime_str(self.end))

			if (self.start >= self.end):
				self.start = self.end - timedelta(minutes = 30)
				self.start_button.set_label(datetime_str(self.start))

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
	def __init__(self, common):
		Gtk.Button.__init__(self)

		add_img = Gtk.Image()
		add_img.set_from_file("client/view/image/add.png")
		self.add(add_img)

		self.connect("clicked", self.on_clicked)

		self.common = common

	def on_clicked(self, button):
		self.launch_add_event()

	def launch_add_event(self, ex_event = None):
		dia = AddEventDialog(self.common, ex_event)
		valide = False
		while(not(valide)):
			if dia.run() == Gtk.ResponseType.OK:
				if ex_event is not None:
					ex_event.delete()
				agenda = self.common.agenda_displayed.value ### TODO TODO TODO : choisir pour les groupes
				event = Event.new(self.common.collection, dia.start, dia.end, dia.name, dia.description, set(), set())
				events = agenda.all_events(event.start, event.end)
				if self.no_conflict(events):
					agenda.add_event(event)
					self.common.event_clicked.value[self.common.agenda_displayed] = event
					valide = True
				else:
					if self.conflicts_with_indispensable(events):
						valide = self.manage_spe_conflicts(events)
					else:
						valide = self.manage_std_conflicts(events)
			else:
				valide = True
		dia.destroy()

	def manage_spe_conflicts(self, events_list):
		dialog = SpeConflictDialog(events_list, self.common)
		res = (dialog.run() == Gtk.ResponseType.OK)
		dialog.destroy()
		return res

	def manage_std_conflicts(self, events_list):
		dialog = StdConflictDialog(events_list)
		res = (dialog.run() == Gtk.ResponseType.OK)
		dialog.destroy()
		return res

	def no_conflict(self, events_list):
		return events_list == set()

	def conflicts_with_indispensable(self, events_list):
		for event in events_list:
			if self.indispensable(event):
				return True
		return False

	def indispensable(self, event):
		return (self.common.user_clicked in event.users)

	def manage_std_conflicts(self, events_list):
		dialog = StdConflictDialog(events_list)
		res = (dialog.run() == Gtk.ResponseType.OK)
		dialog.destroy()
		return res

class AddEvent(Gtk.HBox):
	def __init__(self, common):
		Gtk.HBox.__init__(self)

		self.add(UserFilter(common))
		self.add(ResourceFilter(common))
		self.add(AddEventButton(common))
