# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .link_as_button import *
from client import *
from .observer import *
import re

class RegistrationBox(Gtk.Grid, ViewObserver):

	def __init__(self, common):
		super(Gtk.Grid).__init__()
		super(ViewObserver).__init__(common)

		self.set_border_width(20)
		self.set_column_spacing(10)
		self.set_row_spacing(10)

		title = Gtk.HeaderBar()
		title.props.title = "S'inscrire"
		self.ErrLabel = Gtk.Label("")
		nameL= Gtk.Label("Nom d'utilisateur:")
		nameE= Gtk.Entry()
		mailL= Gtk.Label("Adresse e-mail:")
		mailE= Gtk.Entry()
		passwordL = Gtk.Label("Mot de passe:")
		self.passwordE = Gtk.Entry()
		self.passwordE.set_visibility(False)
		confL = Gtk.Label("Confirmez votre mot de passe:")
		self.confE = Gtk.Entry()
		self.confE.set_visibility(False)
		reg = Gtk.Button("S'inscrire")
		reg.connect("clicked", self.registration, nameE, mailE, self.passwordE, self.confE)
		AlrAccount = LinkAsButton("Déjà inscrit? Connectez-vous ici...")
		AlrAccount.connect("activate_link", self.go_to_connection)

		self.attach(title, 0, 0, 4, 1)
		self.attach(self.ErrLabel, 0, 1, 4, 1)
		self.attach(nameL, 0, 2, 2, 1)
		self.attach_next_to(nameE, nameL, Gtk.PositionType.RIGHT, 2, 1)
		self.attach(mailL, 0, 3, 2, 1)
		self.attach_next_to(mailE, mailL, Gtk.PositionType.RIGHT, 2, 1)
		self.attach(passwordL, 0, 4, 2, 1)
		self.attach_next_to(self.passwordE, passwordL, Gtk.PositionType.RIGHT, 2, 1)
		self.attach(confL, 0, 5, 2, 1)
		self.attach_next_to(self.confE, confL, Gtk.PositionType.RIGHT, 2, 1)
		self.attach(reg, 1, 6, 2, 1)
		self.attach(AlrAccount, 0, 7, 4, 1)

	def registration(self, button, name, mail, password, conf):
		str_name = name.get_text().strip()
		str_mail = mail.get_text().strip()
		str_password = password.get_text().strip()
		str_conf = conf.get_text().strip()
		if str_name and str_mail and str_password and str_conf:
			if re.fullmatch(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", str_mail) is not None:
				if str_password == str_conf:
					account = Account.new(self.common.collection, str_name, str_password, str_mail)
					self.common.account.value = account
					self.common.user_clicked.value = None
					self.common.agenda_displayed.value = None
					self.common.event_clicked.value = None
					self.common.day.value = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
					self.common.is_connected.value = True
				else:
					self.InvalidValuesMessage("La confimation de mot de passe ne correspond pas. Veuillez entrer des valeurs valides")
			else:
				self.InvalidValuesMessage("Veuillez entrer une adresse email valide")
		else:
			self.InvalidValuesMessage("Veuillez remplir tous les champs")

	def go_to_connection(self, link):
		self.common.has_account.value = True

	def InvalidValuesMessage(self, msg):
		self.passwordE.set_text("")
		self.confE.set_text("")
		self.ErrLabel.set_markup("<span foreground='red' font_style='italic'>" + msg + "</span>")
