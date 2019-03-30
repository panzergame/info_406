# -*- coding: utf-8 -*-

from .main_frame import *

class Window:
	def __init__(self, common):
		frame = MainFrame(common)
		frame.connect("destroy", Gtk.main_quit)
		frame.show_all()

	def main(self):
		Gtk.main()
