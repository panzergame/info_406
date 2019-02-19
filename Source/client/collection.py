# -*- coding: utf-8 -*-

from core import *

class Extractor:
	def __init__(self, collection, data):
		self.collection = collection
		self.data = data

	def _extract_proxy(self, proxy):
		return DataProxy(proxy["id"], supported_types_name[proxy["type"]], self.collection)

	def _extract(self, value):
		# En cas de dictionnaire avec id et type, on identifie un data proxy.
		if type(value) == dict:
			if "id" in value and "type" in value:
				return self._extract_proxy(value)

		return value

	def __getitem__(self, key):
		return self._extract(self.data[key])

class ClientCollection(Collection):
	"""
	Collection spécialisé pour faire des appelle au serveur
	et créer des données avec les réponses du serveur.
	"""
	def __init__(self, server):
		super().__init__()

		self.server = server

	def _load(self, _id, type):
		dict_data = self.server.load(_id, type.__name__)
		data = Extractor(self, dict_data)

		if type == User:
			return User(_id, data["first_name"], data["last_name"], data["email"], \
			   data["tel"], data["agenda"])
		elif type == Agenda:
			return Agenda(_id, data["name"], set(data["events"]), set(data["linked_agendas"]))
