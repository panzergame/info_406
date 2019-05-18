# -*- coding: utf-8 -*-

from .dataproxy import *
from .account import *
from .agenda import *
from .user import *
from .resource import *
from .group import *
from .notification import *
from .typedict import *

import re

class Collection:
	""" Collection de toutes les données du système.
	À chaque accès à un data proxy n'ayant pas chargé sa data
	la collection est appellé pour la charger.

	Ceci est possible depuis une BDD ou par réseau, d'où deux
	classes filles de la classe Collection.
	"""

	# Tous les types supportés.
	supported_types = [
		Account,
		Agenda,
		Event,
		Group,
		User,
		Resource,
		Notification
	]

	def __init__(self):
		# Toutes les données existant dynamiquement ou dans le base et chargé.
		self._datas = TypeDict(self.supported_types)
		self._new_datas = TypeDict(self.supported_types)
		# Tous les proxies de données fournis.
		self._data_proxies = TypeDict(self.supported_types)

		# Liste d'attente pour l'écriture et la modification.
		self.new_queue = set()
		self.update_queue = set()
		self.update_relations_queue = set()
		self.delete_queue = set()

	def _register_data(self, data):
		assert(data.id != -1)

		self._datas[data.data_type][data.id] = data

	def _unregister_data(self, data):
		assert(data.id != -1)

		self._datas[data.data_type].pop(data.id)

	def _register_proxy(self, proxy):
		self._data_proxies[proxy.data_type][proxy.id] = proxy

	def _unregister_proxy(self, proxy):
		self._data_proxies[proxy.data_type].pop(proxy.id)

	def _delete_proxies(self, proxies):
		for proxy in proxies:
			proxy.delete()

	def load(self, proxy):
		""" Charge une données d'un proxy """
		raise NotImplementedError

	def load_events(self, agenda, from_date, to_date):
		""" Charge des événements débutant entre deux dates """
		raise NotImplementedError

	def load_last_events(self, agenda, from_date, to_date):
		raise NotImplementedError

	def load_groups(self, sub_name):
		groups = set()

		regex = re.compile(".*{}.*".format(sub_name))
		for group in self._datas[Group].values():
			if regex.match(group.name):
				groups.add(group)

		for group in self._new_datas[Group].values():
			if regex.match(group.name):
				groups.add(group)

		return groups


	def load_users(self, sub_name):
		users = set()

		regex = re.compile(".*{}.*".format(sub_name))
		for user in self._datas[User].values():
			if (regex.match(user.first_name) or regex.match(user.last_name)):
				users.add(user)

		for user in self._new_datas[User].values():
			if (regex.match(user.first_name) or regex.match(user.last_name)):
				users.add(user)

		return users


	def new(self, type, args, kwargs):
		_type = self._datas.key(type)
		data = _type(-1, self, *args, **kwargs)
		self.new_queue.add(data)
		self._new_datas[type][id(data)] = data

		return data

	def _data_or_proxy(self, id, _type):
		""" Conversion d'un identifiant en donné ou proxy """
		if id is None:
			return None

		# Recherche d'une donnée déjà existante.
		data = self._datas[_type].get(id, None)
		if data is not None:
			return data

		# Recherche d'un proxy déjà existant.
		proxy = self._data_proxies[_type].get(id, None)
		if proxy is not None:
			return proxy

		# Création d'un nouveau proxy.
		proxy = DataProxy(id, _type, self)
		# Enregistrement du proxy.
		self._data_proxies[_type][id] = proxy

		return proxy

	def find_proxies(self, _type, _id):
		""" Détection des proxies qui devrait être supprimés
		après la suppression d'une donnée parent.
		Par exemple la suppression d'un Account doit supprimer
		les proxies User obtenus par les groupes.
		"""

		raise NotImplementedError

	def delete(self, data, delete_proxies):
		self.delete_queue.add(data)

		if data.id != -1:
			# Désenregistrement de la donnée.
			self._unregister_data(data)

			if delete_proxies:
				proxies = self.find_proxies(data.data_type, data.id)
				self._delete_proxies(proxies)

				return proxies

		return set()

	def delete_proxy(self, proxy, delete_proxies):
		self.delete_queue.add(proxy)
		# Désenregistrement du proxy.
		self._unregister_proxy(proxy)

		if delete_proxies:
			proxies = self.find_proxies(proxy.data_type, proxy.id)
			self._delete_proxies(proxies)

			return proxies

	def update(self, data):
		self.update_queue.add(data)

	def update_relations(self, data):
		self.update_relations_queue.add(data)

	def flush(self):
		raise NotImplementedError
