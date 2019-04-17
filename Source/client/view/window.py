# -*- coding: utf-8 -*-

from .main_frame import *
from .connection_frame import *


class Window:
	def __init__(self, common):

		self.common = common

		if self.common.is_connected:
			self.frame = MainFrame(self.common)
			self.connected = True
		else:
			self.frame = ConnectionWindow(self.common)
			self.connected = False
		self.frame.connect("destroy", Gtk.main_quit)
		self.frame.show_all()
		self.common.add_observer(self)

	def update(self, common):
		if self.frame.get_property("visible") and self.connected != common.is_connected:
			self.frame.destroy()
			win = Window(common)
			win.main()

	def main(self):
		Gtk.main()
