from .account import *
from .agenda import *
from .slot import *
from .user import *
from .group import *

class Collection:
	""" Collection de toutes les données du système.
	À chaque accès à un data proxy n'ayant pas chargé sa data
	la collection est appellé pour la charger.

	Ceci est possible depuis une BDD ou par réseau, d'où deux
	classe fille de la classe Collection.
	"""

	# Tous les types supporté.
	supported_types = [
		Account,
		Agenda,
		Event,
		Group,
		Slot,
		User
	]

	def __init__(self):
		self._datas = {type : {} for type in self.supported_types}

	def _load(self, id, type):
		pass

	def load(self, id, type):
		""" Charge une données selon son type et id. """
		category = self._datas[type]
		if id not in category:
			category[id] = self._load(id, type)
		return category[id]

	def sync(self):
		""" Enregistre toutes les données. """
		pass
