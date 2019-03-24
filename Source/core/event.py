# -*- coding: utf-8 -*-

from .data import *
from .dataproperty import *
from datetime import *

class Event(Data):
	start = DataProperty("start")
	end = DataProperty("end")
	type = DataProperty("type")
	description = DataProperty("description")
	agenda = DataProperty("agenda")
	creation_date = DataProperty("creation_date")

	def __init__(self, _id, collection, start, end, type, description, resources, users, agenda=None, creation_date=datetime.now()):
		super().__init__(_id, collection)

		self._start = start
		self._end = end
		self._type = type
		self._description = description
		self.resources = resources
		self.users = users
		self._agenda = agenda
		self._creation_date = creation_date

	def update(self):
		# Actualisation de la date de dernière modification.
		self._creation_date = datetime.now()

		super().update()

	@property
	def duration(self):
		return self.end - self.start

	def add_user(self, user):
		# Ajout d'un utilisateur
		self.users.add(user)
		# Modification d'une relation
		self.update_relations()

	def remove_user(self, user):
		# Suppression d'un utilisateur
		self.users.discard(user)
		# Modification d'une relation
		self.update_relations()

	def add_resource(self, resource):
		# Ajout d'une ressource
		self.resources.add(resource)
		# Modification d'une relation
		self.update_relations()

	def remove_resource(self, resource):
		# Suppression d'une ressource
		self.resources.discard(resource)
		# Modification d'une relation
		self.update_relations()

	def __repr__(self):
		def datetime_str(date):
			return date.strftime("%Y-%m-%d %H:%M")

		return "{} {} -> {} ({})".format(self.type, datetime_str(self.start), datetime_str(self.end), self.duration)
