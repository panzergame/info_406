from .agenda import *
from .data import *

class User(Data):
	def __init__(self, _id, collection, first_name, last_name, email, tel, agenda, groups, account=None):
		super().__init__(_id, collection)

		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.tel = tel
		self._agenda = agenda
		self.groups = groups
		self.account = account

	def __repr__(self):
		return "{} {} {} groupes".format(self.first_name, self.last_name, len(self.groups))

	@property
	def agenda(self):
		return self._agenda

	@agenda.setter
	def agenda(self, agenda):
		self._agenda = agenda
		self._agenda.owner = self

	def _add_group(self, group):
		self.groups.add(group)

	def _remove_group(self, group):
		self.groups.discard(group)

	def delete(self):
		super().delete()

		# Suppression de son agenda.
		self.agenda.delete()
