from .data import *

class Event(Data):
	def __init__(self, _id, collection, slot, type, description, resources, users, agenda=None):
		super().__init__(_id, collection)

		self.slot = slot
		self.type = type
		self.description = description
		self.resources = resources
		self.users = users
		self.agenda = agenda

	def __repr__(self):
		return "{} {}".format(self.type, self.slot)
