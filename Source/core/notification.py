# -*- coding: utf-8 -*-

from .data import *
from .dataproperty import *

class Notification(Data):
	AWAITING_COLLISION = "En collision avec un événement personnel" # En collision avec un événement du même agenda et en attente d'une décision.
	AWAITING_COLLISION_REMOTE = "En collision avec un événement distant" # En collision avec un événement d'un agenda distant.
	REJECTED = "Rejeté" # Rejeté définitivement.
	AWAITING_NO_COLLISION = "En attente" # Sans collision mais en attente d'une décision.
	ACCEPTED = "Accepté" # Accepté définitivement.
	INVALID = "Invalid" # Pas encore affecté.

	event = DataOwnerProperty("event")
	agenda = DataOwnerProperty("agenda")
	status = DataProperty("status")

	def __init__(self, _id, collection, event, agenda, status):
		super().__init__(_id, collection)

		self._event = DataOwnerProperty.init(event, self)
		self._agenda = DataOwnerProperty.init(agenda, self)
		self._status = status

	def __repr__(self):
		return "({}, {}, {})".format(self.event, self.agenda, self.status)
