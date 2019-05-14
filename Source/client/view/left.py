import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .search import *
from .account import *
from .group import *
from .add_group import *

class LeftBox(Gtk.VBox):
	"""Partie Gauche de l'écran, avec les utilisateurs, les groupes (en attente de Xavier), et la zeone de recherche"""
	def __init__(self, common):
		super().__init__()

		self.add(AccountBox(common))
		self.add(AddGroupButton(common))
		self.add(SearchBox(common))
