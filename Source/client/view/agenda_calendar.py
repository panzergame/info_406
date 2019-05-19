# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from datetime import *
from .common import *

class AgendaCalendar(Gtk.Button):
	def __init__(self, common):
		Gtk.Button.__init__(self)

		self.common = common

		self.calendar = Gtk.Calendar()
		date = self.common.day.value
		self.calendar.select_month(date.month-1, date.year)
		self.calendar.select_day(date.day)
		self.calendar.connect("day_selected", self.on_changed)

		self.popover = Gtk.Popover()
		self.popover.add(self.calendar)
		self.popover.set_position(Gtk.PositionType.BOTTOM)

		self.label = Gtk.Label(date_to_day_str(date))
		self.add(self.label)
		self.connect("clicked", self.on_clicked)

	def on_clicked(self, button):
		self.popover.set_relative_to(self)
		self.popover.show_all()
		self.popover.popup()

	def on_changed(self, widget):
		year, month, day = self.calendar.get_date()
		month+=1
		#Pour que month soit entre 1 et 12 au lieu d'entre 0 et 11
		#et que le format day/month/year soit en accord avec les datetime
		date = datetime(year, month, day)
		self.label.set_text(date_to_day_str(date))
		self.common.day.value = date
