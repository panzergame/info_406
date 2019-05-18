# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .link_as_button import *
from client import *



class ConnectionBox(Gtk.Grid):

	def __init__(self, common):

		Gtk.Grid.__init__(self)

		self.common = common

		self.set_border_width(20)
		self.set_column_spacing(10)
		self.set_row_spacing(10)

		title = Gtk.HeaderBar()
		title.props.title = "Accéder à mon agenda"
		self.ErrLabel = Gtk.Label("")
		nameL= Gtk.Label("Nom d'utilisateur:")
		nameE= Gtk.Entry()
		passwordL = Gtk.Label("Mot de passe:")
		self.passwordE = Gtk.Entry()
		self.passwordE.set_visibility(False)
		memory = Gtk.CheckButton("Se souvenir de moi")
		connection = Gtk.Button("Se connecter")
		connection.connect("clicked", self.connection, nameE, self.passwordE)
		noAccount = LinkAsButton("Par encore de compte? Inscrivez-vous ici...")
		noAccount.connect("activate_link", self.go_to_registration)


		self.attach(title, 0, 0, 4, 1)
		self.attach(self.ErrLabel, 0, 1, 4, 1)
		self.attach(nameL, 0, 2, 2, 1)
		self.attach_next_to(nameE, nameL, Gtk.PositionType.RIGHT, 2, 1)
		self.attach(passwordL, 0, 3, 2, 1)
		self.attach_next_to(self.passwordE, passwordL, Gtk.PositionType.RIGHT, 2, 1)
		self.attach(memory, 0, 4, 4, 1)
		self.attach(connection, 1, 5, 2, 1)
		self.attach(noAccount, 0, 6, 4, 1)

	def go_to_registration(self, button):
		self.common.has_account.value = False

	def connection(self, link, name, password):
		str_name = name.get_text()
		str_password = password.get_text()
		try:
			account = self.common.collection.load_account(str_name, str_password)
			self.common.account.value = account
			self.common.user_clicked.value = list(self.common.account.value.users)[0]
			self.common.agenda_displayed.value = self.common.user_clicked.value.agenda
			self.common.event_clicked.value = {}
			self.common.day.value = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
			self.common.is_connected.value = True
		except ValueError:
			self.InvalidAccountMessage()

	def InvalidAccountMessage(self):
		self.passwordE.set_text("")
		self.ErrLabel.set_markup("<span foreground='red' font_style='italic'>Identifiant ou mot de passe incorrect. Veuillez réessayer.</span>")
