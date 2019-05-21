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
		self._notifications = WeakRefSet(notifications)
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

		return set(event
				for chunk in chunks
					for event in chunk
						if event.intersect_range(from_date, to_date))

	def notifications_accepted(self, from_date, to_date):
		return set(notif.event
				for notif in self._notifications
					if notif.status == Notification.ACCEPTED and notif.event.intersect_range(from_date, to_date))

	def event_is_accepted(self, event):
		"""Teste si un évènement externe à l'agenda a été accepté par l'utilisateur"""
		return event in (self.notifications_accepted(event.start, event.end))

	def all_events(self, from_date, to_date):
		""" Renvoi tous les évenement avec ceux des agendas liés accepté """
		return self.events(from_date, to_date) | self.notifications_accepted(from_date, to_date)

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
		""" Recherche de collision avec un évenement propre """

		events = set()
		for _event in self.events(event.start, event.end):
			if _event is not event and event.intersect(_event):
				events.add(_event)

		return events

	def notification_intersect(self, event):
		""" Recherche de collision avec un évenement distant """

		notifs = set()
		for notif in self._notifications:
			if notif.event is not event and event.intersect(notif.event):
				notifs.add(notif)

		return notifs

	def sync_notifications(self):
		""" Créer des notifications pour les nouveau événements extérieurs. """

		"""

		1 : Récuperer tout les nouveaux événements distant
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
			for notif in self._notifications:
				if notif.event is event:
					break
			else:
				notification = Notification.new(self.collection, event, self, Notification.INVALID)
				new_notifications.add(notification)

		self._notifications |= new_notifications

		# ==== 3 ====

		# Calcul des collisions.
		for notif in self._notifications:
			# Recherche de collision avec les événement propre à l'agenda.
			self_intersect_events = self.event_intersect(notif.event)
			# Recherche de collision avec les autres notifications (= événement distant).
			remote_intersect_notifs = self.notification_intersect(notif.event)

			# En collision avec un événement propre de l'agenda.
			if len(self_intersect_events) > 0:
				print(self_intersect_events)
				notif.status = Notification.AWAITING_COLLISION
			# En collision avec un autre événement distant.
			elif len(remote_intersect_notifs) > 0:
				notif.status = Notification.AWAITING_COLLISION_REMOTE
			# Sinon pour une nouvelle notification pas de collision du tout.
			elif notif.status == Notification.INVALID:
				notif.status = Notification.AWAITING_NO_COLLISION
			# Une ancienne notification plus en collision.
			elif notif.status in (Notification.AWAITING_COLLISION, Notification.AWAITING_COLLISION_REMOTE):
				notif.status = Notification.AWAITING_NO_COLLISION

			notif.self_intersected_events = self_intersect_events
			notif.remote_intersected_notifs = remote_intersect_notifs

	def notifications(self, now):
		""" Obtention de notifications après now """
		notifications = set()
		for notif in self._notifications:
			event = notif.event
			if event.end >= now:
				notifications.add(notif)

		return notifications

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
		for notif in self._notifications:
			if notif.agenda is agenda:
				euthanazy_notifications.add(notif)

		self._notifications -= euthanazy_notifications
