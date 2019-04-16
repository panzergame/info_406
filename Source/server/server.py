# -*- coding: utf-8 -*-

from core import *
from .converter import *

def log_net(*args):
	print("[net]", *args)

def log_net_func(func):
	def new_func(*args):
		log_net(func.__name__)
		return func(*args)

	return new_func

class Server:
	def __init__(self, collection):
		self.collection = collection
		self.converter = XMLConverter(self.collection)

		# Liste des noms des types supportés et leur association.
		self.supported_types_name = {type.db_table : type for type in self.collection.supported_types}

	def _function_to_xml(self, func, *args):
		data = func(*args)

		return self.converter.to_xml(data)

	@log_net_func
	def find_proxies(self, type_name, _id):
		_type = self.supported_types_name[type_name]

		proxies = self.collection.find_proxies(_type, _id)
		proxy_dict = {type.db_table : set() for type in self.collection.supported_types}

		for proxy in proxies:
			proxy_dict[proxy.data_type.db_table].add(proxy.id)

		# Conversion en dictionnaire de listes pour le XML.
		proxy_dict_list = {name : list(values) for name, values in proxy_dict.items()}
		return proxy_dict_list

	@log_net_func
	def load(self, _id, type_name):
		type = self.supported_types_name[type_name]

		return self._function_to_xml(self.collection.load, _id, type)

	@log_net_func
	def load_account(self, login, mdp):
		return self._function_to_xml(self.collection.load_account, login, mdp)

	@log_net_func
	def load_events(self, agenda_id, from_date, to_date):
		agenda = self.collection.load(agenda_id, Agenda)
		return self._function_to_xml(self.collection.load_events,
				agenda, from_date, to_date)

	@log_net_func
	def load_last_events(self, agenda_id, from_date, to_date):
		agenda = self.collection.load(agenda_id, Agenda)
		return self._function_to_xml(self.collection.load_last_events,
				agenda, from_date, to_date)

	@log_net_func
	def load_groups(self, sub_name):
		return self._function_to_xml(self.collection.load_groups, sub_name)

	@log_net_func
	def flush(self, new_datas, update_datas, update_relation_datas, delete_datas, delete_proxies):
		log_net("New", new_datas)
		log_net("Update", update_datas)
		log_net("Update relations", update_relation_datas)
		log_net("Delete", delete_datas)
		log_net("Delete proxies", delete_proxies)
