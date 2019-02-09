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

	def sync(self):
		""" Enregistre toutes les données. """
		pass
