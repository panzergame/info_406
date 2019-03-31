# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *

from datetime import *

def datetime_str(date):
	return date.strftime("%d/%m/%Y à %H:%M")

class NotificationBox(Gtk.Frame):
	def __init__(self):
		super().__init__()

		box = Gtk.VBox()

		self.title = Gtk.Label()
		self.description = Gtk.Label()
		self.creation = Gtk.Label()
		self.agenda = Gtk.Label()

		scroll = Gtk.ScrolledWindow()
		scroll.add(self.description)

		box.add(self.title)
		box.add(Gtk.Label("Description"))
		box.add(scroll)
		box.add(Gtk.Label("Crée le"))
		box.add(self.creation)
		box.add(Gtk.Label("Agenda parent"))
		box.add(self.agenda)

		self.add(box)
		self.show_all()

	def update(self, notification):

		if notification is not None:
			event = notification.event
			agenda = notification.agenda
			print(notification)
			self.title.set_text(event.type)
			self.description.set_text(event.description)
			self.creation.set_text(datetime_str(event.creation_date))
			self.agenda.set_text(agenda.name)

class NotificationListBox(Gtk.Box):
	def __init__(self, common):
		Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

		self.common = common
		self.common.add_observer(self)
		self.notification = NotificationBox()

		self.list = Gtk.ListStore(str, str, str, object)

		view = Gtk.TreeView(self.list)

		event_column = Gtk.TreeViewColumn("Événement", Gtk.CellRendererText(), text=0)
		agenda_column = Gtk.TreeViewColumn("Agenda", Gtk.CellRendererText(), text=1)
		creation_column = Gtk.TreeViewColumn("Ajouté le", Gtk.CellRendererText(), text=2)

		view.append_column(event_column)
		view.append_column(agenda_column)
		view.append_column(creation_column)

		select = view.get_selection()
		select.connect("changed", self.on_notification_changed)

		sync_button = Gtk.Button("Synchroniser")
		sync_button.connect("clicked", self.on_sync_clicked)

		scroll = Gtk.ScrolledWindow()
		scroll.add(view)
		scroll.set_property("expand", True)

		self.add(sync_button)
		self.add(scroll)
		self.add(self.notification)
		self.set_property("expand", True)

		self.update(common)

	def update(self, common):
		self.list.clear()
		for notification in common.agenda_displayed.notifications:
			event = notification.event
			agenda = notification.agenda
			self.list.append([event.type, agenda.name, datetime_str(event.creation_date), notification])

		self.notification.update(None)

	def on_notification_changed(self, selection):
		model, iter = selection.get_selected()
		if iter is not None:
			notification = model[iter][3]
			self.notification.update(notification)
		else:
			self.notification.update(None)

	def on_sync_clicked(self, button):
		self.common.agenda_displayed.sync_notifications()

