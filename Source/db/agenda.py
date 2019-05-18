# -*- coding: utf-8 -*-

from core import *
from .data import *
from .event import *

class DbAgenda(Agenda, DbData):
	db_attr_names = ("name", "group", "user")
	db_table = "Agenda"

	def __init__(self, *args):
		super().__init__(*args)

	@classmethod
	def db_delete_proxies(cls, collection, _id):
		from .event import DbEvent
		from .notification import DbNotification
		return collection._euthanasy_proxies(DbEvent, "agenda", _id) | \
		collection._euthanasy_proxies(DbNotification, "agenda", _id)
		return set()

	def db_insert_relations(self):
		col = self.collection
		col._insert_linked_agenda(self.id, self._linked_agendas)

	@staticmethod
	def db_delete_relations(collection, id):
		collection._delete_relation(id, "Agenda_Agenda", "agenda1")
		collection._delete_relation(id, "Agenda_Agenda", "agenda2")
