# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .event import EventBox
from .notification import NotificationListBox

class RightBox(Gtk.Frame):
	def __init__(self, common):
		super().__init__()

		event = EventBox(common)
		notification = NotificationListBox(common)

		page1 = Gtk.Box()
		page1.add(event)

		page2 = Gtk.Box()
		page2.add(notification)

		notebook = Gtk.Notebook()
		notebook.append_page(page1, Gtk.Label('Événement'))
		notebook.append_page(page2, Gtk.Label('Notifications'))

		self.add(notebook)

