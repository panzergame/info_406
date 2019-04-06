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
	User,
	Resource,
]

supported_types_name = {type.__name__ : type for type in supported_types}

class Collection:
	""" Collection de toutes les données du système.
	À chaque accès à un data proxy n'ayant pas chargé sa data
	la collection est appellé pour la charger.

	Ceci est possible depuis une BDD ou par réseau, d'où deux
	classes filles de la classe Collection.
	"""

	def load(self, proxy):
		""" Charge une données d'un proxy """
		pass

	def load_events(self, agenda, from_date, to_date):
		""" Charge des événements débutant entre deux dates """
		pass

	def new(self, type, *args):
		pass

	def delete(self, data):
		pass

	def delete_proxy(self, proxy):
		pass

	def update(self, data):
		pass

	def update_relations(self, data):
		pass
