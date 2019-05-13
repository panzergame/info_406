# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *

from datetime import *

def datetime_str(date):
	return date.strftime("%d/%m/%Y à %H:%M")

class NotificationBox(Gtk.ListBox):
	def __init__(self, common):
		super().__init__()

		self.common = common

		self.title = Gtk.Label()
		self.description = Gtk.Label()
		self.creation = Gtk.Label()
		self.agenda = Gtk.Label()

		scroll = Gtk.ScrolledWindow()
		scroll.add(self.description)

		row = Gtk.ListBoxRow()
		box = Gtk.HBox()
		box.add(Gtk.Label("Type", xalign=0))
		box.add(self.title)
		row.add(box)
		self.add(row)

		row = Gtk.ListBoxRow()
		box = Gtk.HBox()
		box.add(Gtk.Label("Description", xalign=0))
		box.add(scroll)
		row.add(box)
		self.add(row)

		row = Gtk.ListBoxRow()
		box = Gtk.HBox()
		box.add(Gtk.Label("Crée le", xalign=0))
		box.add(self.creation)
		row.add(box)
		self.add(row)

		row = Gtk.ListBoxRow()
		box = Gtk.HBox()
		box.add(Gtk.Label("Agenda parent", xalign=0))
		box.add(self.agenda)
		row.add(box)
		self.add(row)

		row = Gtk.ListBoxRow()
		box = Gtk.HBox()

		accept = Gtk.Button("Accepter")
		accept.connect("clicked", self.on_accept_clicked)

		deny = Gtk.Button("Refuser")
		deny.connect("clicked", self.on_deny_clicked)
		
		box.add(accept)
		box.add(deny)

		row.add(box)
		self.add(row)

		self.show_all()

	def on_accept_clicked(self, button):
		agenda = self.notification.agenda # TODO depuis notification.accept() ?
		agenda.remove_notification(self.notification, False)
		self.common._notify()

	def on_deny_clicked(self, button):
		agenda = self.notification.agenda # TODO depuis notification.accept() ?
		agenda.remove_notification(self.notification, True)
		self.common._notify()

	def update(self, notification):
		self.notification = notification

		if notification is not None:
			event = notification.event

			self.title.set_text(event.type)
			self.description.set_text(event.description)
			self.creation.set_text(datetime_str(event.creation_date))
			self.agenda.set_text(event.agenda.name)
			self.set_opacity(1)
		else:
			self.set_opacity(0)

class NotificationListBox(Gtk.Box):
	def __init__(self, common):
		Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

		self.common = common
		self.common.add_observer(self)
		self.notification = NotificationBox(self.common)

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
		if common.agenda_displayed is not None:
			for notification in common.agenda_displayed.notifications:
				event = notification.event
				self.list.append([event.type, event.agenda.name, datetime_str(event.creation_date), notification])

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
		self.common._notify() # TODO

