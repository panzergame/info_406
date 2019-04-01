# -*- coding: utf-8 -*-

from core import *
from .data import *
from .event import *

class DbAgenda(Agenda, DbData):
	db_attr_names = ("name", "group", "user", "last_sync")
	db_table = "Agenda"

	def __init__(self, *args):
		super().__init__(*args)

	@classmethod
	def db_delete_proxies(cls, collection, _id):
		collection._delete_proxies(Event, "agenda", _id)
		collection._delete_proxies(Notification, "agenda", _id)

	def db_insert_relations(self):
		col = self.collection
		col._insert_relation(self.id, self.linked_agendas, "Agenda_Agenda", "agenda1", "agenda2")
		col._insert_relation(self.id, self.ignored_events, "Agenda_Ignore_Event", "agenda", "event")

	@staticmethod
	def db_delete_relations(collection, id):
		collection._delete_relation(id, "Agenda_Agenda", "agenda1")
		collection._delete_relation(id, "Agenda_Agenda", "agenda2")
		collection._delete_relation(id, "Agenda_Ignore_Event", "agenda")

	def delete(self, owner):
		pass # TODO events
