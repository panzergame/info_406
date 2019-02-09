from .data import *

class Event(Data):
	def __init__(self, _id, slot, type="", description="", resources=set(), users=set()):
		super().__init__(_id)

		self.slot = slot
		self.type = type
		self.description = description
		self.resources = resources
		self.users = users

	def __repr__(self):
		return "{} {}".format(self.type, self.slot)
