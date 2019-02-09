from .data import *

class Resource(Data):
	def __init__(self, _id, name, location, capacity):
		super().__init__(_id)

		self.name = name
		self.location = location
		self.capacity = capacity
