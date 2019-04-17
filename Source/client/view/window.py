# -*- coding: utf-8 -*-

from .main_frame import *
from .connection_frame import *


class Window:
	def __init__(self, common):

		self.common = common

		self.frame = self.choose_frame()

		self.frame.connect("destroy", Gtk.main_quit)
		self.frame.show_all()
		self.common.add_observer(self)

	def choose_frame(self):
		if self.common.is_connected:
			frame = MainFrame(self.common)
		else:
			frame = ConnectionWindow(self.common)
		return frame

	def update(self, common):
		self.frame.hide()
		win = Window(common)
		win.main()

	def main(self):
		Gtk.main()
