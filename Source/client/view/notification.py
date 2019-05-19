# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *
from .common import *
from .observer import *
from datetime import *

def datetime_str(date):
	return date.strftime("%d/%m/%Y à %H:%M")

class NotificationBox(Gtk.ListBox, ViewObserver):
	def __init__(self, common):
		Gtk.ListBox.__init__(self)
		ViewObserver.__init__(self, common, common.notification_clicked)

		self.title = Gtk.Label()
		self.description = Gtk.Label()
		self.date = Gtk.Label()
		self.creation = Gtk.Label()
		self.status = Gtk.Label()
		self.agenda = Gtk.Label()
		self.intersect_list = Gtk.ListStore(str, str, str, object)
		self.intersect_view = Gtk.TreeView(self.intersect_list)

		type_column = Gtk.TreeViewColumn("Type", Gtk.CellRendererText(), text=0)
		date_column = Gtk.TreeViewColumn("Date", Gtk.CellRendererText(), text=1)
		creation_column = Gtk.TreeViewColumn("Crée le", Gtk.CellRendererText(), text=2)

		self.intersect_view.append_column(type_column)
		self.intersect_view.append_column(date_column)
		self.intersect_view.append_column(creation_column)

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
		box.add(Gtk.Label("Date", xalign=0))
		box.add(self.date)
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
		box.add(Gtk.Label("État", xalign=0))
		box.add(self.status)
		row.add(box)
		self.add(row)

		row = Gtk.ListBoxRow()
		box = Gtk.HBox()
		box.add(Gtk.Label("Agenda parent", xalign=0))
		box.add(self.agenda)
		row.add(box)
		self.add(row)

		row = Gtk.ListBoxRow()
		box = Gtk.VBox()
		box.add(Gtk.Label("En conflit avec", xalign=0))
		scroll = Gtk.ScrolledWindow()
		scroll.add(self.intersect_view)
		box.add(scroll)
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

	def on_accept_clicked(self, button):
		notif = self.common.notification_clicked.value
		if len(notif.self_intersected_events) > 0:
			dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.WARNING,
				Gtk.ButtonsType.OK, "Attention")
			dialog.format_secondary_text("Cette action supprimera les événéments en conflits")

			if dialog.run() == Gtk.ResponseType.OK:
				notif.accept()
			dialog.destroy()
		else:
			notif.accept()

		self.common.notification_clicked.notify()

	def on_deny_clicked(self, button):
		self.common.notification_clicked.value.reject()
		self.common.notification_clicked.notify()

	def update(self):
		notif = self.common.notification_clicked.value

		if notif is not None:
			event = notif.event

			self.title.set_text(event.type)
			self.description.set_text(event.description)
			self.date.set_text(event_to_date_str(event.start, event.end))
			self.creation.set_text(datetime_str(event.creation_date))
			self.agenda.set_text(event.agenda.name)
			self.status.set_text(notif.status)

			self.intersect_list.clear()
			for _event in notif.self_intersected_events:
				self.intersect_list.append((_event.type, event_to_date_str(_event.start, _event.end),
						datetime_str(_event.creation_date), _event))

			self.show()
		else:
			self.hide()

class NotificationListBox(Gtk.VBox, ViewObserver):
	def __init__(self, common):
		Gtk.Box.__init__(self)
		ViewObserver.__init__(self, common, common.agenda_displayed)

		notification = NotificationBox(common)

		"""
						1			2			3			4 (objet)
			Group							date_modif
				Agenda						date_modif
					En collision			date_modif
						Accepté				date_modif
							type	date	date_modif
						En attente
					Sans collision
						Accepté
						En attente
		"""
		self.tree = Gtk.TreeStore(str, str, str, object)

		self.view = Gtk.TreeView(self.tree)

		event_column = Gtk.TreeViewColumn("", Gtk.CellRendererText(), text=0)
		date_column = Gtk.TreeViewColumn("Date", Gtk.CellRendererText(), text=1)
		creation_column = Gtk.TreeViewColumn("Ajouté le", Gtk.CellRendererText(), text=2)

		self.view.append_column(event_column)
		self.view.append_column(date_column)
		self.view.append_column(creation_column)
		select = self.view.get_selection()
		select.connect("changed", self.on_notification_changed)

		sync_button = Gtk.Button("Synchroniser")
		sync_button.connect("clicked", self.on_sync_clicked)

		scroll = Gtk.ScrolledWindow()
		scroll.add(self.view)
		scroll.set_property("expand", True)

		self.pack_start(sync_button, False, False, False)
		self.add(scroll)
		self.pack_end(notification, False, False, False)
		self.set_property("expand", True)

	def update(self):
		self.tree.clear()

		# On tri les notifications par group/agenda/status/notification
		dr = {}
		ag = self.common.agenda_displayed.value
		if ag is not None:
			for notification in sorted(ag.notifications(datetime.now()), key = lambda notif : (notif.event.start, notif.event.creation_date)):
				event = notification.event
				agenda = event.agenda
				group = agenda.group
				if group is not None:
					dg = get_or_init(dr, group, {})
					da = get_or_init(dg, agenda, {})
					dc = get_or_init(da, notification.status, [])
					dc.append(notification)

		# On rempli le model Gtk
		for group, agendas in dr.items():
			giter = self.tree.append(None, (group.name, "", "", group))
			for agenda, categories in agendas.items():
				aiter = self.tree.append(giter, (agenda.name, "", "", agenda))
				for category, notifs in categories.items():
					citer = self.tree.append(aiter, (category, "", "", None))
					for notif in notifs:
						self.tree.append(citer, (notif.event.type, event_to_date_str(notif.event.start, notif.event.end), datetime_str(notif.event.creation_date), notif))

		self.view.expand_all()

	def on_notification_changed(self, selection):
		model, iter = selection.get_selected()
		if iter is not None:
			item = model[iter][3]
			if isinstance(item, Notification):
				self.common.notification_clicked.value = item
			else:
				self.common.notification_clicked.value = None
		else:
			self.common.notification_clicked.value = None

	def on_sync_clicked(self, button):
		self.common.agenda_displayed.value.sync_notifications()
		self.common.notification_clicked.value = None

		self.update()

