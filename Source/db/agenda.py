# -*- coding: utf-8 -*-

from core import *
from .data import *
from .event import *
from datetime import *
from dateutil.relativedelta import *

class DbAgenda(Agenda, DbData):
	db_attr_names = ("name", "group", "user")
	db_table = "Agenda"

	def __init__(self, *args):
		super().__init__(*args)

		# Cache d'événement par block d'un mois.
		# En réalité par block de tous événements commencant dans le même mois.
		self.chunks = {}

	def db_insert_relations(self):
		col = self.collection
		col._insert_relation(self.id, self.linked_agendas, "Agenda_Agenda", "agenda1", "agenda2")

	def db_delete_relations(self):
		col = self.collection
		col._delete_relation(self.id, "Agenda_Agenda", "agenda1")
		col._delete_relation(self.id, "Agenda_Agenda", "agenda2")

	def _get_chunk(self, month_first_day, next_month_first_day):
		""" Obtention d'une page d'événement grace à la
		date du premier jour du mois et la date du premier
		jour du mois suivant
		"""

		# Vérification dans le cache.
		chunk = self.chunks.get(month_first_day, None)
		if chunk is not None:
			return chunk

		""" Chargement direct (sans passer par un DataProxy) de
		Tous les événements commencant dans le mois.
		"""
		col = self.collection
		events = col.load_batched(DbEvent, "agenda", self.id,
				"AND (start >= \"{}\" AND start < \"{}\")".format(month_first_day, next_month_first_day))

		# Enregistrement de la page en cache.
		self.chunks[month_first_day] = events

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
		super().add_event(event)

		# Ajout dans le chunk.
		chunk = self._get_chunks(event.start, event.start)[0]
		chunk.add(event)

	def remove_event(self, event):
		super().remove_event(event)

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

		return events

	def delete(self, owner):
		pass # TODO events
