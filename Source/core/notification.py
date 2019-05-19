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
		self._self_intersected_events = WeakRefSet(set())
		self._remote_intersected_notifs = WeakRefSet(set())

	def __repr__(self):
		return "({}, {}, {})".format(self.event, self.agenda, self.status)

	def accept(self):
		""" Accepte la notification et refuse les événements/notification
		en conflit """
		self.status = self.ACCEPTED

		# Suppression des événements en conflit.
		for event in self.self_intersected_events:
			self.agenda.remove_event(event)
		# Refus des notifications en conflit.
		for notif in self.remote_intersected_notifs:
			notif.reject()

	def reject(self):
		""" Refuse la notification """
		self.status = self.REJECTED

	@property
	def self_intersected_events(self):
		return self._self_intersected_events

	@self_intersected_events.setter
	def self_intersected_events(self, events):
		self._self_intersected_events = WeakRefSet(events)

	@property
	def remote_intersected_notifs(self):
		return self._remote_intersected_notifs

	@remote_intersected_notifs.setter
	def remote_intersected_notifs(self, notifs):
		self._remote_intersected_notifs = WeakRefSet(notifs)
