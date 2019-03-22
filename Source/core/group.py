# -*- coding: utf-8 -*-

from .data import *
from .dataproperty import *

class Group(Data):
	name = DataProperty("name")

	def __init__(self, _id, collection, name, admins, subscribers, agendas, resources):
		super().__init__(_id, collection)

		self._name = name
		self.admins = admins
		self.subscribers = subscribers
		self.agendas = agendas
		self.resources = resources

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
		# Modification d'une relation
		self.update_relations()

	def unsubscribe(self, user):
		""" Desinscription d'un utilisateur. """
		self.subscribers.discard(user)
		# Suppression du groupe dans l'utilisateur.
		user._remove_group(self)
		# Modification d'une relation
		self.update_relations()

	def is_admin(self, user):
		""" Test si un utilisateur est administrateur. """
		return user in self.admins

	def add_admin(self, user):
		""" Ajout d'un administrateur. """
		self.admins.add(user)
		# Modification d'une relation
		self.update_relations()

	def remove_admin(self, user):
		""" Suppression d'un administrateur. """
		self.admins.discard(user)
		# Modification d'une relation
		self.update_relations()

	def delete(self):
		super().delete()

		# Destruction de tous le agendas.
		for agenda in self.agendas:
			agenda.delete()

		# Destruction de toutes les ressources.
		for resource in self.resources:
			resource.delete()
			
