# -*- coding: utf-8 -*-

from .event import *
from .notification import *
from .data import *
from .dataproperty import *
from datetime import *
from dateutil.relativedelta import *

class Agenda(Data):
	name = DataProperty("name")
	last_sync = DataProperty("last_sync")
	user = DataOwnerProperty("user")
	group = DataOwnerProperty("group")

	def __init__(self, _id, collection, name, linked_agendas, notifications, ignored_events,
			  last_sync=None, user=None, group=None):
		super().__init__(_id, collection)

		self._name = name
		self.linked_agendas = WeakRefSet(linked_agendas, self)
		self.notifications = WeakRefSet(notifications)
		self.ignored_events = WeakRefSet(ignored_events, self)
		self._user = DataOwnerProperty.init(user, self)
		self._group = DataOwnerProperty.init(group, self)
		if last_sync is None:
			self._last_sync = datetime.now()
		else:
			self._last_sync = last_sync

		# Cache d'événement par block d'un mois.
		# En réalité par block de tous événements commencant dans le même mois.
		self._chunks = {}

		# Cache des événements récents.
		self._last_events = WeakRefSet()
		self._last_events_date = None

	def __repr__(self):
		return self.name

	def _get_chunk(self, month_first_day, next_month_first_day):
		""" Obtention d'une page d'événement grace à la
		date du premier jour du mois et la date du premier
		jour du mois suivant
		"""

		# Vérification dans le cache.
		chunk = self._chunks.get(month_first_day, None)
		if chunk is not None:
			return chunk

		""" Chargement direct (sans passer par un DataProxy) de
		Tous les événements commencant dans le mois.
		"""
		col = self.collection
		events = col.load_events(self, month_first_day, next_month_first_day)

		# Enregistrement de la page en cache.
		self._chunks[month_first_day] = WeakRefSet(events)

		return events

	def _get_chunks(self, from_date, to_date):
		""" Obtention de tous les chunks couvrant la periode
		from_date à to_date
		"""

		chunks = []
		# Le permier jour du mois actuel.
		month_first_day = datetime(from_date.year, from_date.month, 1)
		# Tant que le prochains chunk a une date inférieur à to_date.
		while month_first_day < to_date:
			# Le premier jour du mois suivant.
			next_month_first_day = month_first_day + relativedelta(months=1)
			chunks.append(self._get_chunk(month_first_day, next_month_first_day))
			# Passage au mois suivant.
			month_first_day = next_month_first_day

		return chunks

	def add_event(self, event):
		""" Ajout d'un evenement. """
		# Actualisation de son propriétaire.
		event.agenda = self

		# Ajout dans le chunk.
		chunk = self._get_chunks(event.start, event.start)[0]
		chunk.add(event)

		# Ajout d'un événement récent
		self._last_events.add(event)

	def remove_event(self, event):
		""" Suppression d'un evenement. """
		# Actualisation de son propriétaire.
		event.agenda = None

		# Suppression dans le chunk.
		chunk = self._get_chunks(event.start, event.start)[0]
		chunk.discard(event)

	def events(self, from_date, to_date):
		""" Obtention des événements propre à l'agenda sur
		une période
		"""
		chunks = self._get_chunks(from_date, to_date)

		events = set()
		for chunk in chunks:
			for event in chunk:
				if event.start >= from_date and event.start < to_date:
					events.add(event)

		return events

	def all_events(self, from_date, to_date):
		""" Renvoi tous les évenement avec ceux des agendas liés """
		events = self.events(from_date, to_date)
		for agenda in self.linked_agendas:
			events |= agenda.all_events(from_date, to_date)

		return (events - self.ignored_events)

	def last_events(self, last_date):
		# Chargement de plus d'événements récent.
		if self._last_events_date is None or last_date < self._last_events_date:
			self._last_events |= self.collection.load_last_events(self, last_date, self._last_events_date)
			self._last_events_date = last_date
	
		last_events = set()
		for event in self._last_events:
			if event.creation_date >= last_date:
				last_events.add(event)

		return last_events

	def sync_notifications(self):
		""" Créer des notifications pour les nouveau événements extérieurs. """

		# Les derniers événements des agendas liée.
		last_events = set()
		# Récupération des derniers événements.
		for agenda in self.linked_agendas:
			last_events |= agenda.last_events(self.last_sync)

		# Création des notifications.
		for event in last_events:
			notification = Notification.new(self.collection, event, self)
			self.notifications.add(notification)

		self.last_sync = datetime.now()

	def add_notification(self, notification):
		""" Ajout d'une notification de cet agenda. """
		self.notifications.add(notification)

	def remove_notification(self, notification, ignore):
		""" Suppression d'une notification de cet agenda. """
		self.notifications.discard(notification)
		if ignore:
			self.ignored_events.add(notification.event)

	def link_agenda(self, agenda):
		""" Ajout d'un lien vers un autre agenda. """
		self.linked_agendas.add(agenda)

	def unlink_agenda(self, agenda):
		""" Suppression d'un lien vers un autre agenda. """
		self.linked_agendas.discard(agenda)
