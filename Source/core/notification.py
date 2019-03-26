# -*- coding: utf-8 -*-

from .data import *
from .dataproperty import *

class Notification(Data):
	event = DataWeakProperty("event")
	agenda = DataWeakProperty("agenda")

	def __init__(self, _id, collection, event, agenda):
		super().__init__(_id, collection)

		self._event = DataWeakProperty.init(event, self)
		self._agenda = DataWeakProperty.init(agenda, self)
