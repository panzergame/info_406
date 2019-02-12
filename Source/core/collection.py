from .account import *
from .agenda import *
from .slot import *
from .user import *
from .group import *

# Tous les types supporté.
supported_types = [
	Account,
	Agenda,
	Event,
	Group,
	Slot,
	User
]

supported_types_name = {type.__name__ : type for type in supported_types}

class Collection:
	""" Collection de toutes les données du système.
	À chaque accès à un data proxy n'ayant pas chargé sa data
	la collection est appellé pour la charger.

	Ceci est possible depuis une BDD ou par réseau, d'où deux
	classe fille de la classe Collection.
	"""

	def __init__(self):
		self._datas = {type : {} for type in supported_types}

	def _load(self, _id, type):
		pass

	def load(self, _id, type):
		""" Charge une données selon son type et id. """
		category = self._datas[type]
		if _id not in category:
			category[_id] = self._load(_id, type)
		return category[_id]

	def _new(self, data, type):
		pass

	def new(self, data, type):
		self._new(data, type)

		category = self._datas[type]
		category[data.id] = data

		return data

	def _delete(self, data, type):
		pass

	def delete(self, data, type):
		self._delete(data, type)
		print(self._datas[type])
		self._datas[type].pop(data.id)

	def _update(self, data, type):
		pass

	def update(self, data, type):
		self._update(data, type)
