# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .link_as_button import *


class RegistrationBox(Gtk.Grid):

	def __init__(self):

		Gtk.Grid.__init__(self)
		self.set_border_width(20)
		self.set_column_spacing(10)
		self.set_row_spacing(10)

		title = Gtk.HeaderBar()
		title.props.title = "S'inscrire à [comment ça s'apppelle ?!]"
		nameL= Gtk.Label("Nom d'utilisateur:")
		nameE= Gtk.Entry()
		mailL= Gtk.Label("Adresse e-mail:")
		mailE= Gtk.Entry()
		passwordL = Gtk.Label("Mot de passe:")
		passwordE = Gtk.Entry()
		confL = Gtk.Label("Confirmez votre mot de passe:")
		confE = Gtk.Entry()
		reg = Gtk.Button("S'inscrire")
		reg.connect("clicked", self.registration)
		AlrAccount = LinkAsButton("","Déjà inscrit? Connectez-vous ici...")
		AlrAccount.connect("activate_link", self.go_to_connection)

		self.attach(title, 0, 0, 4, 1)
		self.attach(nameL, 0, 1, 2, 1)
		self.attach_next_to(nameE, nameL, Gtk.PositionType.RIGHT, 2, 1)
		self.attach(mailL, 0, 2, 2, 1)
		self.attach_next_to(mailE, mailL, Gtk.PositionType.RIGHT, 2, 1)
		self.attach(passwordL, 0, 3, 2, 1)
		self.attach_next_to(passwordE, passwordL, Gtk.PositionType.RIGHT, 2, 1)
		self.attach(confL, 0, 4, 2, 1)
		self.attach_next_to(confE, confL, Gtk.PositionType.RIGHT, 2, 1)
		self.attach(reg, 1, 5, 2, 1)
		self.attach(AlrAccount, 0, 6, 4, 1)

	def registration(self, button):
		print("registration")

	def go_to_connection(self, link):
		print("go_to_connection")
