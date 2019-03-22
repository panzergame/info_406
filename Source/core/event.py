# -*- coding: utf-8 -*-

from .data import *
from .dataproperty import *

class Event(Data):
	start = DataProperty("start")
	end = DataProperty("end")
	type = DataProperty("type")
	description = DataProperty("description")
	agenda = DataProperty("agenda")

	def __init__(self, _id, collection, start, end, type, description, resources, users, agenda=None):
		super().__init__(_id, collection)

		self._start = start
		self._end = end
		self._type = type
		self._description = description
		self.resources = resources
		self.users = users
		self._agenda = agenda

	@property
	def duration(self):
		return self.end - self.start

	def __repr__(self):
		return "{} {} -> {} ({})".format(self.type, self.start, self.end, self.duration)
