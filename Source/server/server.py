# -*- coding: utf-8 -*-

from core import *
from .converter import *

class Server:
	def __init__(self, collection):
		self.collection = collection
		self.converter = XMLConverter(self.collection)

		# Liste des noms des types supportés et leur association.
		self.supported_types_name = {type.db_table : type for type in self.collection.supported_types}

	def _function_to_xml(self, func, *args):
		data = func(*args)

		return self.converter.to_xml(data)

	def find_proxies(self, _type, _id):
		proxies = self.collection.find_proxies(_type, _id)
		proxy_dict = {type.db_name : set() for type in self.collection.supported_types}

		for proxy in proxies:
			proxy_dict[proxy.data_type.db_name].add(proxy.id)

		return proxy_dict

	def load(self, _id, type_name):
		print("load", _id, type_name)
		type = supported_types_name[type_name]

		return self._function_to_xml(self.collection.load, _id, type)

	def load_account(self, login, mdp):
		print("load account", login)
		return self._function_to_xml(self.collection.load_account, login, mdp)

	def load_events(self, agenda_id, from_date, to_date):
		print("load events")

		agenda = self.collection.load(agenda_id, Agenda)
		return self._function_to_xml(self.collection.load_events,
				agenda, from_date, to_date)

	def load_last_events(self, agenda_id, from_date, to_date):
		print("load last events")

		agenda = self.collection.load(agenda_id, Agenda)
		return self._function_to_xml(self.collection.load_last_events,
				agenda, from_date, to_date)

	def load_groups(self, sub_name):
		print("load groups")
		return self._function_to_xml(self.collection.load_groups, sub_name)

	def flush(self, new_datas, update_datas, delete_datas):
		print("New", new_datas)
		print("Update", update_datas)
		print("Delete", delete_datas)
