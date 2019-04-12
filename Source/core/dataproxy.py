# -*- coding: utf-8 -*-

from .dataweak import *

""" Classe d'une donnée non chargé de la base de donnée
Chaque proxy est identifié par une id (int) et utilise une collection pour charger
la donnée identifié lors d'un accèss à un membre de la donnée.
"""
class DataProxy(WeakRefered):
	def __init__(self, _id, type, collection):
		super().__init__()

		self._id = _id
		self._type = type
		self._collection = collection

	@property
	def id(self):
		return self._id

	@property
	def data_type(self):
		return self._type

	@property
	def collection(self):
		return self._collection

	@property
	def __class__(self):
		return self._type

	def delete(self, owner=None, destruct_data=True):
		super().delete()

		if destruct_data and "_data" in dir(self):
			self._data.delete(owner, destruct_proxy=False)

		self._collection.delete_proxy(self)

	def __getattr__(self, name):
		# Chargement de la donnée pour la première fois.
		if "_data" not in dir(self):
			self._data = self._collection.load(self._id, self._type)
			self._data.proxy = self

		return getattr(self._data, name)

	def __setattr__(self, name, value):
		# Ne pas prendre en compte les attributs privées.
		if name[0] == '_':
			object.__setattr__(self, name, value)
		else:
			# Chargement de la donnée pour la première fois.
			if "_data" not in dir(self):
				self._data = self._collection.load(self._id, self._type)
				self._data.proxy = self

			return setattr(self._data, name, value)

	def __repr__(self):
		if "_data" not in dir(self):
			return "[Proxy of {} type {}]".format(self._id, self._type.__name__)
		else:
			return self._data.__repr__()

	def __hash__(self):
		return hash(self._type) ^ hash(self._id)

	def __eq__(self, other):
		return hash(self) == hash(other)
