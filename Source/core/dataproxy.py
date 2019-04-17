# -*- coding: utf-8 -*-

from .dataweak import *

class DataProxy(WeakRefered):
	""" Classe d'une donnée non chargé de la base de donnée
	Chaque proxy est identifié par une id (int) et utilise une collection pour charger
	la donnée identifié lors d'un accèss à un membre de la donnée.
	"""

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

	def delete(self, owner=None, destruct_data=True, delete_proxies=True):
		super().delete()

		if destruct_data and "_data" in dir(self):
			self._data.delete(owner, destruct_proxy=False)

		self._collection.delete_proxy(self, delete_proxies)

	def __getattr__(self, name):
		# Chargement de la donnée pour la première fois.
		if "_data" not in dir(self):
			data = self._collection.load(self._id, self._type)
			self._data = data
			self._data.proxy = self

		return getattr(self._data, name)

	def __setattr__(self, name, value):
		# Ne pas prendre en compte les attributs privées.
		if name[0] == '_':
			object.__setattr__(self, name, value)
		else:
			# Chargement de la donnée pour la première fois.
			if "_data" not in dir(self):
				data = self._collection.load(self._id, self._type)
				self._data = data
				self._data.proxy = self

			return setattr(self._data, name, value)

	def __repr__(self):
		if "_data" not in dir(self):
			return "[Proxy of {} type {}, {}]".format(self._id, self._type.__name__, hex(id(self)))
		else:
			return self._data.__repr__()

	def __hash__(self):
		return hash(self._type) ^ hash(self._id)

	def __eq__(self, other):
		return hash(self) == hash(other)
