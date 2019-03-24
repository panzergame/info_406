# -*- coding: utf-8 -*-

from .event import *
from .data import *
from .dataproperty import *

class Agenda(Data):
	name = DataProperty("name")
	user = DataWeakProperty("user")
	group = DataWeakProperty("group")

	def __init__(self, _id, collection, name, linked_agendas, user=None, group=None):
		super().__init__(_id, collection)

		self._name = name
		self.linked_agendas = WeakRefList(self, linked_agendas)
		self._user = DataWeakProperty.init(user, self)
		self._group = DataWeakProperty.init(user, self)

	def __repr__(self):
		return self.name

	def add_event(self, event):
		""" Ajout d'un evenement. """
		# Actualisation de son propriétaire.
		event.agenda = self

	def remove_event(self, event):
		""" Suppression d'un evenement. """
		# Actualisation de son propriétaire.
		event.agenda = None

	def link_agenda(self, agenda):
		""" Ajout d'un lien vers un autre agenda. """
		self.linked_agendas.add(agenda)

	def unlink_agenda(self, agenda):
		""" Suppression d'un lien vers un autre agenda. """
		self.linked_agendas.discard(agenda)
