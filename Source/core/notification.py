# -*- coding: utf-8 -*-

from .data import *
from .dataproperty import *

class Notification(Data):
	event = DataOwnerProperty("event")
	agenda = DataOwnerProperty("agenda")
	status = DataOwnerProperty("status")

	def __init__(self, _id, collection, event, agenda, status):
		super().__init__(_id, collection)

		self._event = DataOwnerProperty.init(event, self)
		self._agenda = DataOwnerProperty.init(agenda, self)
		self._status = DataOwnerProperty.init(status, self)

	def __repr__(self):
		return "({}, {}, {})".format(self.event, self.agenda, self.status)
