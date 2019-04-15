# -*- coding: utf-8 -*-

from core import *
from .converter import *

def log_net(*args):
	print("[net]", *args)

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
		log_net("load", _id, type_name)
		type = self.supported_types_name[type_name]

		return self._function_to_xml(self.collection.load, _id, type)

	def load_account(self, login, mdp):
		log_net("load account", login)
		return self._function_to_xml(self.collection.load_account, login, mdp)

	def load_events(self, agenda_id, from_date, to_date):
		log_net("load events")

		agenda = self.collection.load(agenda_id, Agenda)
		return self._function_to_xml(self.collection.load_events,
				agenda, from_date, to_date)

	def load_last_events(self, agenda_id, from_date, to_date):
		log_net("load last events")

		agenda = self.collection.load(agenda_id, Agenda)
		return self._function_to_xml(self.collection.load_last_events,
				agenda, from_date, to_date)

	def load_groups(self, sub_name):
		log_net("load groups")
		return self._function_to_xml(self.collection.load_groups, sub_name)

	def flush(self, new_datas, update_datas, update_relation_datas, delete_datas, delete_proxies):
		log_net("New", new_datas)
		log_net("Update", update_datas)
		log_net("Update relations", update_relation_datas)
		log_net("Delete", delete_datas)
		log_net("Delete proxies", delete_proxies)
