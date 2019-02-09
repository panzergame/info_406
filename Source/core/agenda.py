from .event import *
from .data import *

class Agenda(Data):
	def __init__(self, _id, name, events=set(), linked_agendas=set()):
		super().__init__(_id)

		self.name = name
		self.events = events
		self.linked_agendas = linked_agendas

	def create_event(self, *args):
		self.events.add(Event(*args))

	def delete_event(self, event):
		self.events.discard(event)

	def link_agenda(self, agenda):
		self.linked_agendas.add(agenda)

	def unlink_agenda(self, agenda):
		self.linked_agendas.discard(agenda)

	@property
	def all_events(self):
		""" Renvoi tous les évenement avec ceux des agendas liés """
		events = self.events
		for agenda in self.linked_agendas:
			events |= agenda.all_events

		return events

	def __repr__(self):
		return self.name
