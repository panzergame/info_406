# -*- coding: utf-8 -*-

from .data import *
from .dataproperty import *
from datetime import *

class Event(Data):
	start = DataProperty("start")
	end = DataProperty("end")
	type = DataProperty("type")
	description = DataProperty("description")
	agenda = DataOwnerProperty("agenda")
	creation_date = DataProperty("creation_date")

	def __init__(self, _id, collection, start, end, type, description, resources=set(), users=set(), agenda=None, creation_date=None):
		"""Création d'un évènement
			@param collection : la collection à passer (dans le fichier common).
			...

		"""

		super().__init__(_id, collection)

		self._start = start
		self._end = end
		self._type = type
		self._description = description
		self.resources = WeakRefSet(resources, self)
		self.users = WeakRefSet(users, self)
		self._agenda = DataOwnerProperty.init(agenda, self)
		if creation_date is None:
			self._creation_date = datetime.now()
		else:
			self._creation_date = creation_date

	def update(self):
		""" Actualisation de la date de dernière modification."""
		self._creation_date = datetime.now()

		super().update()

	@property
	def duration(self):
		"""return la durée de l'évènement """
		return self.end - self.start

	@property
	def start(self):
		return self._start

	@property
	def end(self):
		return self._end

	def add_user(self, user):
		"""Ajout d'un utilisateur sur un event"""
		self.users.add(user)

	def remove_user(self, user):
		"""suppression de la participation d'un utilisateur à un évènement"""
		self.users.discard(user)

	def add_resource(self, resource):
		"""Ajout d'une ressource pour un event"""
		self.resources.add(resource)

	def remove_resource(self, resource):
		"""Suppression d'une ressource pour un event"""
		self.resources.discard(resource)

	def intersect(self, event):
		""" Test l'intersection entre deux événements """
		return self.intersect_range(event.start, event.end)

	def intersect_range(self, start, end):
		return start <= self.start < end or \
			   start < self.end < end or \
			   self.start <= start < self.end or \
			   self.start < end < self.end

	def __repr__(self):
		"""affiche l'event"""
		def datetime_str(date):
			return date.strftime("%Y-%m-%d %H:%M")

		return "{} {} -> {} ({})".format(self.type, datetime_str(self.start), datetime_str(self.end), self.duration)
