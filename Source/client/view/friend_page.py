# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

from .search_friend_box import *
from .observer import *

class FriendPage(Gtk.ScrolledWindow):
	def __init__(self, common):
		Gtk.ScrolledWindow.__init__(self)

		box = Gtk.VBox()

		self.search = SearchFriendBox(common)
		#self.friends = FriendList(common)

		box.pack_start(self.search, False, False, False)
		#box.pack_start(self.friends, False, False, False)

		self.add(box)
