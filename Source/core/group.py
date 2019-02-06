from .data import *

class Group(Data):
	def __init__(self, id, admins=set(), subscribers=set(), agendas={}):
		super().__init__(id)

		self._admins = admins
		self.subscribers = subscribers
		self._agendas = agendas

	def create_agenda(self, name):
		agenda = Agenda(name)
		self._agendas[name] = agenda

		return agenda

	def delete_agenda(self, name):
		del self._agendas[name]

	def find_agenda(self, name, default=None):
		return self._agendas.get(name, default)

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
