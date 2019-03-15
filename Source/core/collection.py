# -*- coding: utf-8 -*-

from .account import *
from .agenda import *
from .user import *
from .resource import *
from .group import *

# Tous les types supportés.
supported_types = [
	Account,
	Agenda,
	Event,
	Group,
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

	def load(self, _id, type):
		""" Charge une données selon son type et id. """
		pass

	def new(self, data, type):
		pass

	def delete(self, data, type):
		pass

	def update(self, data, type):
		pass
