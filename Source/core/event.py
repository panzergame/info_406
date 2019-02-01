from .data import *

class Event(Data):
	def __init__(self, slot, type, description):
		super().__init__()

		self.slot = slot
		self.type = type
		self.description = description

	def __repr__(self):
		return "{} {}".format(self.type, self.slot)
