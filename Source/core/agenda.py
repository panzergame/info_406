# -*- coding: utf-8 -*-

from .event import *
from .linkedagenda import *
from .notification import *
from .data import *
from .dataproperty import *
from datetime import *
from dateutil.relativedelta import *

class Agenda(Data):
	name = DataProperty("name")
	user = DataOwnerProperty("user")
	group = DataOwnerProperty("group")

	def __init__(self, _id, collection, name, linked_agendas=set(), notifications=set(),
			  user=None, group=None):
		"""Création d'un agenda.
			@param collection : la collection a passer (dans le fichier common).
			@param name : nom de l'agenda
			@param linked_agendas : liste des agendas associés à l'agenda.
			@param notifications : liste des notifications liés à l'agenda.
			@param ignored_events : les évènements ni en attentes ?
			"""

		super().__init__(_id, collection)

		self._name = name
		self._linked_agendas = WeakRefSet(linked_agendas, self)
		self.notifications = WeakRefSet(notifications)
		self._user = DataOwnerProperty.init(user, self)
		self._group = DataOwnerProperty.init(group, self)

		# Cache d'événement par block d'un mois.
		# Ces blocs continennent tous les événements recouvrant une partie d'un même mois.
		# Si il existe des événements entre deux mois sur plusieurs jour, alors ils sont
		# doublé dans les chunks de ces deux mois.
		self._chunks = {}

		# Cache des événements récents.
		self._last_events = WeakRefSet()
		self._last_events_date = None

	def __repr__(self):
		"""affiche l'agenda"""
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
		events = WeakRefSet(col.load_events(self, month_first_day, next_month_first_day))

		# Enregistrement de la page en cache.
		self._chunks[month_first_day] = events

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

	@property
	def linked_agendas(self):
		return set(map(lambda x : x.agenda, self._linked_agendas))

	def add_event(self, event):
		""" Ajout d'un evenement. """
		# Actualisation de son propriétaire.
		event.agenda = self

		# Ajout dans les chunks.
		for chunk in self._get_chunks(event.start, event.end):
			chunk.add(event)

		# Ajout d'un événement récent
		self._last_events.add(event)

	def remove_event(self, event):
		""" Suppression d'un evenement. """
		# Actualisation de son propriétaire.
		event.agenda = None

		# Suppression dans les chunks.
		for chunk in self._get_chunks(event.start, event.end):
			chunk.discard(event)

		# Suppression d'un potentielle événement récent
		self._last_events.discard(event)

	def events(self, from_date, to_date):
		""" Obtention des événements propre à l'agenda sur
		une période
		"""
		chunks = self._get_chunks(from_date, to_date)

		events = set()
		for chunk in chunks:
			for event in chunk:
				if event.intersect_range(from_date, to_date):
					events.add(event)

		return events

	def all_events(self, from_date, to_date):
		""" Renvoi tous les évenement avec ceux des agendas liés """
		events = self.events(from_date, to_date)
		for agenda in self.linked_agendas:
			events |= agenda.all_events(from_date, to_date)

		return (events)# - self.ignored_events)

	def last_events(self, last_date):
		""" Chargement de plus d'événements récent """
		if self._last_events_date is None or last_date < self._last_events_date:
			self._last_events |= self.collection.load_last_events(self, last_date, self._last_events_date)
			self._last_events_date = last_date

		last_events = set()
		for event in self._last_events:
			if event.creation_date >= last_date:
				last_events.add(event)

		return last_events

	def event_intersect(self, event):
		for _event in self.all_events(event.start, event.end):
			if event.intersect(_event):
				return True

		return False

	def sync_notifications(self):
		""" Créer des notifications pour les nouveau événements extérieurs. """

		"""
		
		1 : Récuperer tout les événements distant
		2 : Création des notifications
		3 : Calcul de collision sur les notifications
		
		"""

		# ==== 1 ====

		# Les derniers événements des agendas liées.
		last_events = set()
		# Récupération des derniers événements.
		for linked_agenda in self._linked_agendas:
			last_events |= linked_agenda.agenda.last_events(linked_agenda.last_sync)
			linked_agenda.last_sync = datetime.now()

		# ==== 2 ====

		# Les nouvelles notifications.
		new_notifications = set()

		# Création des notifications.
		for event in last_events:
			# Si un événement à été modifié, on ne doit pas recréer une notification.
			for notif in self.notifications:
				if notif.event is event:
					notif.status = Notification.INVALID
					break
			else:
				notification = Notification.new(self.collection, event, self, Notification.INVALID)
				new_notifications.add(notification)

		self.notifications |= new_notifications

		# ==== 3 ====

		# Calcul des collisions.
		for notif in self.notifications:
			events = self.events(notif.event.start, notif.event.end)
			for event in events:
				if event.intersect(notif.event):
					notif.status = Notification.AWAITING_COLLISION
					break
			else:
				notif.status = Notification.AWAITING_NO_COLLISION

	def add_notification(self, notification):
		""" Ajout d'une notification de cet agenda. """
		self.notifications.add(notification)

	def remove_notification(self, notification, ignore):
		""" Suppression d'une notification de cet agenda. """
		self.notifications.discard(notification)
		"""if ignore:
			self.ignored_events.add(notification.event)"""

	def link_agenda(self, agenda):
		""" Ajout d'un lien vers un autre agenda. """

		# Utilisation de la plus petite date pour signifier aucune synchronisation.
		self._linked_agendas.add(LinkedAgenda(agenda, datetime(1, 1, 1)))

	def unlink_agenda(self, agenda):
		""" Suppression d'un lien vers un autre agenda. """

		# Suppression de l'agenda lié correspondant.
		for linked_agenda in self._linked_agendas:
			if linked_agenda.agenda is agenda:
				self._linked_agendas.discard(linked_agenda)
				break

		# Suppression des notifications de cet agenda.
		euthanazy_notifications = set()
		for notif in self.notifications:
			if notif.agenda is agenda:
				euthanazy_notifications.add(notif)

		self.notifications -= euthanazy_notifications
