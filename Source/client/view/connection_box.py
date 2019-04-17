# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .link_as_button import *



class ConnectionBox(Gtk.Grid):

	def __init__(self, common):

		Gtk.Grid.__init__(self)

		self.common = common

		self.set_border_width(20)
		self.set_column_spacing(10)
		self.set_row_spacing(10)

		title = Gtk.HeaderBar()
		title.props.title = "Accéder à mon agenda"
		nameL= Gtk.Label("Nom d'utilisateur:")
		nameE= Gtk.Entry()
		passwordL = Gtk.Label("Mot de passe:")
		passwordE = Gtk.Entry()
		memory = Gtk.CheckButton("Se souvenir de moi")
		connection = Gtk.Button("Se connecter")
		connection.connect("clicked", self.connection)
		noAccount = LinkAsButton("", "Par encore de compte? Inscrivez-vous ici...")
		noAccount.connect("activate_link", self.go_to_registration)


		self.attach(title, 0, 0, 4, 1)
		self.attach(nameL, 0, 1, 2, 1)
		self.attach_next_to(nameE, nameL, Gtk.PositionType.RIGHT, 2, 1)
		self.attach(passwordL, 0, 2, 2, 1)
		self.attach_next_to(passwordE, passwordL, Gtk.PositionType.RIGHT, 2, 1)
		self.attach(memory, 0, 3, 4, 1)
		self.attach(connection, 1, 4, 2, 1)
		self.attach(noAccount, 0, 5, 4, 1)

	def go_to_registration(self, button):
		self.common.has_account = False

	def connection(self, link):
		self.common.is_connected = True