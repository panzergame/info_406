# -*- coding: utf-8 -*-

from .data import *

class Event(Data):
	def __init__(self, _id, collection, start, end, type, description, resources, users, agenda=None):
		super().__init__(_id, collection)

		self.start = start
		self.end = end
		self.type = type
		self.description = description
		self.resources = resources
		self.users = users
		self.agenda = agenda

	@property
	def duration(self):
		return self.end - self.start

	def __repr__(self):
		return "{} {} -> {} ({})".format(self.type, self.start, self.end, self.duration)
