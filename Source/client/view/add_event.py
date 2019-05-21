# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .date_time import DateTimeDialog
from core import *
from datetime import datetime
from datetime import timedelta
from .conflict_dialogs import *
from .common import *

class AddResourceList(Gtk.TreeView):
	def __init__(self, resources):
		self.resources = set()
		self.list = Gtk.ListStore(str, str, int, bool, object)

		Gtk.TreeView.__init__(self, self.list)

		name_column = Gtk.TreeViewColumn("Nom", Gtk.CellRendererText(), text=0)
		loc_column = Gtk.TreeViewColumn("Location", Gtk.CellRendererText(), text=1)
		cap_column = Gtk.TreeViewColumn("Capacité", Gtk.CellRendererText(), text=2)
		selected = Gtk.CellRendererToggle()
		selected.connect("toggled", self.on_selected)
		select_column = Gtk.TreeViewColumn("Sélectionné(s)", selected, active=3)

		self.append_column(name_column)
		self.append_column(loc_column)
		self.append_column(cap_column)

		for res in resources:
			self.list.append((res.name, res.location, res.capacity, False, res))

	def on_selected(self, widget, path):
		row = self.list[path]
		row[3] = not row[3]

		res = row[4]

		if row[3]:
			self.resources.add(res)
		else:
			self.resources.discard(res)

class AddUserList(Gtk.TreeView):
	def __init__(self, users):
		self.users = set()
		self.list = Gtk.ListStore(str, str, bool, object)

		Gtk.TreeView.__init__(self, self.list)

		first_name = Gtk.CellRendererText()
		last_name = Gtk.CellRendererText()

		name_column = Gtk.TreeViewColumn("Nom")
		name_column.pack_start(first_name, True)
		name_column.pack_start(last_name, True)
		name_column.add_attribute(first_name, "text", 0)
		name_column.add_attribute(last_name, "text", 1)

		selected = Gtk.CellRendererToggle()
		selected.connect("toggled", self.on_selected)
		select_column = Gtk.TreeViewColumn("Sélectionné(s)", selected, active=2)

		self.append_column(name_column)
		self.append_column(select_column)

		for user in users:
			self.list.append((user.first_name, user.last_name, False, user))

	def on_selected(self, widget, path):
		row = self.list[path]
		row[2] = not row[2]

		user = row[3]

		if row[2]:
			self.users.add(user)
		else:
			self.users.discard(user)

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

		group = self.common.agenda_displayed.value.group
		if group is None:
			users = set()
			resources = set()
		else:
			users = group.subscribers
			resources = group.resources

		self.users_list = AddUserList(users)
		self.resources_list = AddResourceList(resources)

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

		if group is not None:
			box.add(Gtk.Label("Participants"))
			box.add(self.users_list)
			box.add(Gtk.Label("Ressources"))
			box.add(self.resources_list)

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

	@property
	def users(self):
		return self.users_list.users

	@property
	def resources(self):
		return self.resources_list.resources

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
				event = Event.new(self.common.collection, dia.start, dia.end, dia.name, dia.description, dia.resources, dia.users)
				print(event.resources, event.users)
				events = agenda.all_events(event.start, event.end)
				if self.no_conflict(events):
					agenda.add_event(event)
					self.common.event_clicked.value[self.common.agenda_displayed.value] = event
					valide = True
				else:
					if self.conflicts_with_indispensable(events):
						valide = self.manage_spe_conflicts(events)
					else:
						valide = self.manage_std_conflicts(agenda, event, events)
			else:
				valide = True
		dia.destroy()

	def manage_spe_conflicts(self, events_list):
		dialog = SpeConflictDialog(events_list)
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
		return event.is_user(self.common.user_clicked)

	def manage_std_conflicts(self, agenda, event, events_list):
		dialog = StdConflictDialog(event.start, event.end, self.common)
		valide = False
		while(not(valide)):
			response = dialog.run()
			if (response == Gtk.ResponseType.OK):
				res = self.force_creation(agenda, event, events_list)
				valide = res
			elif (response == 1):
				res = self.edit_events(agenda, event, events_list)
				valide = res
			elif (response == 2):
				res = False
				valide = True
			else:
				res = True
				valide = True
		dialog.destroy()
		return res

	def force_creation(self, agenda, event, events_list):
		dialog = ForceRequestDialog()
		if (dialog.run() == Gtk.ResponseType.OK):
			for e in events_list:
				e.delete()
			agenda.add_event(event)
			self.common.event_clicked.value[self.common.agenda_displayed] = event
			res = True
		else:
			res = False
		dialog.destroy()
		return res

	def edit_events(self, agenda, event, events_list):
		dialog = EditEventsDialog(event.start, event.end, self.common)
		valide = False
		while(not(valide)):
			if (dialog.run() == Gtk.ResponseType.OK):
				if (dialog.no_conflicts()):
					dia = EditRequestDialog()
					if (dia.run() == Gtk.ResponseType.OK):
						# Procéder aux changements
						#agenda.add_event(event)
						#self.common.event_clicked.value = event
						res = True
						valide = True
					dia.destroy()
				else:
					dia = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
											"Alerte : Action impossible")
					dia.format_secondary_text("Il reste des conflits non résolus, il ne doit rester "
											  "aucun conflit pour continuer.")
					dia.run()
					dia.destroy()
			else:
				res = False
				valide = True
		dialog.destroy()
		return res
