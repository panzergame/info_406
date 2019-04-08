# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk



class LinkAsButton(Gtk.LinkButton):
	"""LinkButton qui se comporte comme une Button"""

	def __init__(self, method, text):
		Gtk.LinkButton.__init__(self, method, text)

	def do_activate_link(self):
		return True