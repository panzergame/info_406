# -*- coding: utf-8 -*-

from .converter import *

class ClientCollection(Collection):
	def __init__(self, server):
		super().__init__()

		self.converter = XMLConverter(self)
		self.server = server
		self.supported_types_name = {type.__name__ : type for type in self.collection.supported_types}

	def _function_to_data(self, func, *args, _type):
		xml = func(*args)

		return self.converter.to_data(_type, xml)

	def _function_to_datas(self, func, *args, _type):
		xml = func(*args)

		return self.converter.to_datas(_type, xml)

	def find_proxies(self, _type, _id):
		xml = self.server.find_proxies(_type.__name__, _id)

		proxies = set()
		for type_name, category in xml:
			_sub_type = self.supported_types_name[type_name]
			for _id in category:
				data = self.data_or_proxy(_id, _sub_type)
				proxies.add(data)

		return proxies

	def load(self, _id, _type):
		return self._function_to_data(self.server.load,
				_id, _type.__name__, _type)

	def load_account(self, login, mdp):
		return self._function_to_data(self.server.load_account,
				login, mdp, Account)

	def load_events(self, agenda, from_date, to_date):
		if agenda.id == -1:
			return set()

		return self._function_to_datas(self.server.load_events,
				agenda.id, from_date, to_date, Event)

	def load_last_events(self, agenda, from_date, to_date):
		if agenda.id == -1:
			return set()

		return self._function_to_datas(self.server.load_last_events,
				agenda.id, from_date, to_date, Event)

	def load_groups(self, sub_name):
		return super().load_groups(sub_name) |
			self._function_to_datas(self.server.load_groups,
					sub_name)
