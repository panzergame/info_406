# -*- coding: utf-8 -*-

from .converter import *

class ClientCollection(Collection):
	def __init__(self, server):
		super().__init__()

		self.converter = XMLConverter(self)
		self.server = server
		self.supported_types_name = {type.__name__ : type for type in self.supported_types}

	def _convert_to_data(self, _type, xml):
		""" Essaye de convertir un tableau XML en donnée
		Si l'id correspond à une donné déjà existante, il n'y a pas de conversion.
		"""

		# Sécurité pour éviter les rechargements.
		_id = xml["id"]
		data = self._datas[_type].get(_id, None)

		if data is None:
			data = self.converter.to_data(_type, xml)
			# Enregistrement de la nouvelle donnée.
			self._register_data(data)

		return data

	def _function_to_data(self, func, _type, *args):
		xml = func(*args)

		return self._convert_to_data(_type, xml)

	def _function_to_datas(self, func, _type, *args):
		xml = func(*args)

		return {self._convert_to_data(_type, sub_xml) for sub_xml in xml}

	def find_proxies(self, _type, _id):
		xml = self.server.find_proxies(_type.__name__, _id)
		proxies = set()
		for type_name, category in xml.items():
			_sub_type = self.supported_types_name[type_name]
			for _id in category:
				data = self._data_or_proxy(_id, _sub_type)
				proxies.add(data)

		return proxies

	def load(self, _id, _type):
		return self._function_to_data(self.server.load, _type,
				_id, _type.__name__)

	def load_account(self, login, mdp):
		return self._function_to_data(self.server.load_account,
				Account, login, mdp)

	def load_events(self, agenda, from_date, to_date):
		if agenda.id == -1:
			return set()

		return self._function_to_datas(self.server.load_events,
				Event, agenda.id, from_date, to_date)

	def load_last_events(self, agenda, from_date, to_date):
		if agenda.id == -1:
			return set()

		return self._function_to_datas(self.server.load_last_events,
				Event, agenda.id, from_date, to_date)

	def load_groups(self, sub_name):
		return super().load_groups(sub_name) | \
			self._function_to_datas(self.server.load_groups,
					Group, sub_name)

	def flush(self):
		new_queue = self.converter.queue_to_xml(self.new_queue)
		update_queue = self.converter.queue_to_xml(self.update_queue)
		update_relations_queue = self.converter.queue_to_xml(self.update_relations_queue)
		delete_queue = self.converter.queue_to_xml(self.delete_queue)
		delete_proxy_queue = self.converter.queue_to_xml(self.delete_proxy_queue)

		self.server.flush(new_queue, update_queue, update_relations_queue, delete_queue, delete_proxy_queue)
