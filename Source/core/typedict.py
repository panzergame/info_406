# -*- coding: utf-8 -*-

class TypeDict:
	""" Un dictionnaire avec pour clé des types """

	def __init__(self, types):
		self._dict = [(type, {}) for type in types]

	def _get_values(self, key):
		for type, values in self._dict:
			if issubclass(key, type):
				return values

		return None

	def key(self, key):
		for type, _ in self._dict:
			if issubclass(key, type):
				return type

		return None

	def __getitem__(self, key):
		values = self._get_values(key)
		if values is None:
			raise ValueError("Invalid type key {}".format(key))

		return values

	def get(self, key):
		for type, values in self._dict:
			if issubclass(key, type):
				return type, values

		return None, None
