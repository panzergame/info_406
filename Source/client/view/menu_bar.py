# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from client import *


class MenuBar(Gtk.MenuBar):
	def __init__(self, common):
		Gtk.MenuBar.__init__(self)
		self.common = common

		logout = Gtk.MenuItem("Se déconnecter")
		logout.connect("activate", self.disconnect)
		self.add(logout)

	def disconnect(self, link):
		self.common.is_connected = False
		self.common.day = datetime.now()
		self.common.event_clicked = None
		self.common.agenda_displayed = None
		self.common.user_clicked = None
		self.common.account = None
