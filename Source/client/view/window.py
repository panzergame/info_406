# -*- coding: utf-8 -*-

from .main_frame import *
from .connection_frame import *


class Window(ViewObserver):
	def __init__(self, common):
		ViewObserver.__init__(self, common, common.is_connected)

		if self.common.is_connected.value:
			self.frame = MainFrame(self.common)
			self.connected = True
		else:
			self.frame = ConnectionWindow(self.common)
			self.connected = False
		self.frame.connect("destroy", Gtk.main_quit)
		self.frame.show_all()

		# Permet d'initialiser tout le monde
		self.common.notify()

	def update(self):
		if self.frame.get_property("visible") and self.connected != self.common.is_connected.value:
			self.frame.destroy()
			# euuhhh ?
			win = Window(self.common)
			win.main()

	def main(self):
		Gtk.main()
