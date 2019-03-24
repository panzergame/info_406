# -*- coding: utf-8 -*-

from .data import *
from .dataproperty import *

class Account(Data):
	login = DataProperty("login")
	mdp = DataProperty("mdp")
	email = DataProperty("email")

	def __init__(self, _id, collection, users, login, mdp, email):
		super().__init__(_id, collection)

		self.users = users
		self._login = login
		self._mdp = mdp
		self._email = email

	def __repr__(self):
		return "{} [{}]".format(self.login, ", ".join((str(user) for user in self.users)))

	def add_user(self, user):
		""" Ajout d'un utilisateur au compte. """
		self.users.add(user)
		# Actualisation de son proprétaire.
		user.account = self

	def remove_user(self, user):
		""" Suppression d'un utilisateur au compte """
		self.users.discard(user)
		# Actualisation de son proprétaire.
		user.account = None
