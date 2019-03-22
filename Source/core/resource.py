# -*- coding: utf-8 -*-

from .data import *
from .dataproperty import *

class Resource(Data):
	name = DataProperty("name")
	location = DataProperty("location")
	capacity = DataProperty("capacity")
	group = DataProperty("group")

	def __init__(self, _id, collection, name, location, capacity, group):
		super().__init__(_id, collection)

		self._name = name
		self._location = location
		self._capacity = capacity
		self._group = group
