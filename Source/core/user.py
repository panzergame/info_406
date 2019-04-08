# -*- coding: utf-8 -*-

from .agenda import *
from .data import *
from .dataproperty import *

class User(Data):
	first_name = DataProperty("first_name")
	last_name = DataProperty("last_name")
	email = DataProperty("email")
	tel = DataProperty("tel")
	account = DataOwnerProperty("account")

	def __init__(self, _id, collection, first_name, last_name, email, tel, agenda, groups, account=None):
		""" création d'un utilisateur"""

		super().__init__(_id, collection)

		self._first_name = first_name
		self._last_name = last_name
		self._email = email
		self._tel = tel
		self._agenda = agenda
		self.groups = groups
		self._account = DataOwnerProperty.init(account, self)

	def __repr__(self):
		return "{} {} {} groupes".format(self.first_name, self.last_name, len(self.groups))

	@property
	def agenda(self):
		""" return l'agenda de l'utilisateur """
		return self._agenda

	@agenda.setter # Avec DataProperty
	def agenda(self, agenda):
		"""ajoute un agenda a l'utilisateur """
		self._agenda = agenda
		self._agenda.user = self

	def _add_group(self, group):
		""" ajoute un groupe a la liste de groupe de l'utilisateur """
		self.groups.add(group)

	def _remove_group(self, group):
		""" enlève le groupe de sa liste de groupe."""
		self.groups.discard(group)
