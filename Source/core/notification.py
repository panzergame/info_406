# -*- coding: utf-8 -*-

from .data import *
from .dataproperty import *

class Notification(Data):
	AWAITING_COLLISION = "En collision" # En collision et en attente d'une décision.
	REJECTED = "Rejeté" # Rejeté définitivement.
	AWAITING_NO_COLLISION = "En attente" # Sans collision mais en attente d'une décision.
	ACCEPTED = "Accepté" # Accepté définitivement.
	INVALID = "Invalid" # Pas encore affecté.

	event = DataOwnerProperty("event")
	agenda = DataOwnerProperty("agenda")
	status = DataProperty("status")

	def __init__(self, _id, collection, event, agenda, status=INVALID):
		super().__init__(_id, collection)

		self._event = DataOwnerProperty.init(event, self)
		self._agenda = DataOwnerProperty.init(agenda, self)
		self._status = status

	def __repr__(self):
		return "({}, {}, {})".format(self.event, self.agenda, self.status)
