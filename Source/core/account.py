# -*- coding: utf-8 -*-

from .data import *

class Account(Data):
	def __init__(self, _id, collection, users, login, mdp, email):
		super().__init__(_id, collection)

		self.users = users
		self.login = login
		self.mdp = mdp
		self.email = email

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

	def delete(self):
		super().delete()

		# Suppression de tous les utilisateurs.
		for user in self.users:
			user.delete()
