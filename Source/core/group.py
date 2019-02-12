from .data import *

class Group(Data):
	def __init__(self, _id, collection, name, admins, subscribers, agendas):
		super().__init__(_id, collection)

		self.name = name
		self._admins = admins
		self.subscribers = subscribers
		self._agendas = agendas

	def create_agenda(self, name):
		agenda = Agenda.new(self.collection, name, set(), set())
		self._agendas.add(agenda)

		return agenda

	def delete_agenda(self, agenda):
		self._agendas.discard(agenda)

	def subscribe(self, user):
		self.subscribers.add(user)

	def unsubscribe(self, user):
		self.subscribers.discard(user)

	def is_admin(self, user):
		return user in self._admins

	def add_admin(self, user):
		self._admins.add(user)

	def remove_admin(self, user):
		self._admins.discard(user)

	def presence_agenda(self, users, resources):
		pass
