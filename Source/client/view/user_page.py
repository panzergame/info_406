import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .account import *

class UserPage(Gtk.VBox):
	"""Partie Gauche de l'écran, avec les utilisateurs, les groupes (en attente de Xavier), et la zeone de recherche"""
	def __init__(self, common):
		super().__init__()

		self.add(AccountBox(common))
