# -*- coding: utf-8 -*-

from .data import *

class Resource(Data):
	def __init__(self, _id, collection, name, location, capacity, group):
		super().__init__(_id, collection)

		self.name = name
		self.location = location
		self.capacity = capacity
		self.group = group
