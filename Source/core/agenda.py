from .event import *
from .data import *

class Agenda(Data):
	def __init__(self, _id, collection, name, events, linked_agendas, owner=None):
		super().__init__(_id, collection)

		self.name = name
		self.events = events
		self.linked_agendas = linked_agendas
		self.owner = owner

	def __repr__(self):
		return self.name

	def add_event(self, event):
		""" Ajout d'un evenement. """
		self.events.add(event)
		# Actualisation de son propriétaire.
		event.agenda = self

	def remove_event(self, event):
		""" Suppression d'un evenement. """
		self.events.discard(event)
		# Actualisation de son propriétaire.
		event.agenda = None

	def link_agenda(self, agenda):
		""" Ajout d'un lien vers un autre agenda. """
		self.linked_agendas.add(agenda)

	def unlink_agenda(self, agenda):
		""" Suppression d'un lien vers un autre agenda. """
		self.linked_agendas.discard(agenda)

	@property
	def all_events(self):
		""" Renvoi tous les évenement avec ceux des agendas liés """
		events = self.events
		for agenda in self.linked_agendas:
			events |= agenda.all_events

		return events

	def delete(self):
		# TODO enlever les liens des autres agendas : faire une liste d'agenda utilisateurs de celui ci ?

		# Suppression de tous les evenements.
		for event in self.events:
			event.delete()
