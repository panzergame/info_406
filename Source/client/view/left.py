import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .search import SearchBox
from .search_results import SearchResultsBox
from .account import AccountBox
from .group import GroupBox

class LeftBox(Gtk.Box):
	"""Partie Gauche de l'écran, avec les utilisateurs, les groupes (en attente de Xavier), et la zeone de recherche"""
	def __init__(self, common):
		self.common = common
		Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.set_border_width(10)
		self.add(AccountBox(self.common))
		self.add(GroupBox(self.common))
		self.add(SearchBox(self.common))
		self.add(SearchResultsBox(self.common))
		self.show_all()