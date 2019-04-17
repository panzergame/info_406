# -*- coding: utf-8 -*-

from .data import *
from .dataproperty import *

class Group(Data):
	name = DataProperty("name")

	def __init__(self, _id, collection, name, admins=set(), subscribers=set(), agendas=set(), resources=set()):
		super().__init__(_id, collection)

		self._name = name
		self.admins = WeakRefSet(admins, self)
		self.subscribers = WeakRefSet(subscribers, self)
		self.agendas = agendas
		self.resources = WeakRefSet(resources, self)

	def __repr__(self):
		return "{}, {} agendas, {} admins, {} subscribers".format(\
			self.name, len(self.agendas), len(self.admins), len(self.subscribers))

	def add_agenda(self, agenda):
		""" Ajout d'un agenda. """
		self.agendas.add(agenda)
		# Actualisation de son propriétaire.
		agenda.group = self

	def remove_agenda(self, agenda):
		""" Suppression d'un agenda de la liste. """
		self.agendas.discard(agenda)
		# Actualisation de son propriétaire.
		agenda.group = None

	def subscribe(self, user):
		""" Inscription d'un utilisateur. """
		self.subscribers.add(user)
		# Ajout du groupe dans l'utilisateur.
		user._add_group(self)

	def unsubscribe(self, user):
		""" Desinscription d'un utilisateur. """
		self.subscribers.discard(user)
		# Suppression du groupe dans l'utilisateur.
		user._remove_group(self)

	def is_admin(self, user):
		""" Test si un utilisateur est administrateur. """
		return user in self.admins

	def add_admin(self, user):
		""" Ajout d'un administrateur. """
		self.admins.add(user)

	def remove_admin(self, user):
		""" Suppression d'un administrateur. """
		self.admins.discard(user)
