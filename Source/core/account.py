# -*- coding: utf-8 -*-

from .data import *
from .dataproperty import *

class Account(Data):
	login = DataProperty("login")
	mdp = DataProperty("mdp")
	email = DataProperty("email")

	def __init__(self, _id, collection, login, mdp, email, users=set()):
		"""Création d'un compte.
		   @param collection : la collection à passer (dans le fichier common).
		   @param users : liste des users sur le compte
		   @param login : login du compte
		   @param mdp : mdp du compte
		   @param email : email du compte
		   """

		super().__init__(_id, collection)

		self.users = WeakRefSet(users)
		self._login = login
		self._mdp = mdp
		self._email = email

	def __repr__(self):
		"""affiche les users d'un compte"""
		return "{} [{}]".format(self.login, ", ".join((str(user) for user in self.users)))

	def add_user(self, user):
		""" Ajout d'un utilisateur au compte.
			@param user : utilisateur qu'on veut ajouter."""
		self.users.add(user)
		# Actualisation de son proprétaire.
		user.account = self

	def remove_user(self, user):
		""" Suppression d'un utilisateur au compte
		    @param user : utilisateur que l'on veut supprimer """
		self.users.discard(user)
		# Actualisation de son proprétaire.
		user.account = None
