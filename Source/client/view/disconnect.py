# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from client import *


class Disconnect(Gtk.MenuBar):
	def __init__(self, common):
		Gtk.MenuBar.__init__(self)
		self.common = common

		logout = Gtk.MenuItem("Se déconnecter    ")
		logout.connect("activate", self.disconnect)
		self.add(logout)

	def disconnect(self, link):
		self.common.is_connected.value = False
		self.common.day.value = datetime.now()
		self.common.event_clicked.value = None
		self.common.agenda_displayed.value = None
		self.common.user_clicked.value = None
		self.common.account.value = None
