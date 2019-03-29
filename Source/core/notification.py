# -*- coding: utf-8 -*-

from .data import *
from .dataproperty import *

class Notification(Data):
	event = DataOwnerProperty("event")
	agenda = DataOwnerProperty("agenda")

	def __init__(self, _id, collection, event, agenda):
		super().__init__(_id, collection)

		self._event = DataOwnerProperty.init(event, self)
		self._agenda = DataOwnerProperty.init(agenda, self)
