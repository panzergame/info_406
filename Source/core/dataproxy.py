# -*- coding: utf-8 -*-

""" Classe d'une donnée non chargé de la base de donnée
Chaque proxy est identifié par une id (int) et utilise une collection pour charger
la donnée identifié lors d'un accèss à un membre de la donnée.
"""
class DataProxy:
	def __init__(self, _id, type, collection):
		self.__dict__["id"] = _id
		self.__dict__["type"] = type
		self.__dict__["collection"] = collection

	def __getattr__(self, name):
		# Chargement de la donnée pour la première fois.
		if "data" not in self.__dict__ or self.__dict__["data"] is None:
			self.__dict__["data"] = self.__dict__["collection"].load(self.__dict__["id"], self.__dict__["type"])

		return getattr(self.__dict__["data"], name)

	def __setattr__(self, name, value):
		# Chargement de la donnée pour la première fois.
		if "data" not in self.__dict__ or self.__dict__["data"] is None:
			self.__dict__["data"] = self.__dict__["collection"].load(self.__dict__["id"], self.__dict__["type"])

		return setattr(self.__dict__["data"], name, value)

	def __repr__(self):
		if "data" not in self.__dict__ or self.__dict__["data"] is None:
				return "[Proxy of {} type {}]".format(self.__dict__["id"], self.__dict__["type"].__name__)
		else:
			return self.__dict__["data"].__repr__()
