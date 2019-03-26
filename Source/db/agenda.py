# -*- coding: utf-8 -*-

from core import *
from .data import *
from .event import *

class DbAgenda(Agenda, DbData):
	db_attr_names = ("name", "group", "user")
	db_table = "Agenda"

	def __init__(self, *args):
		super().__init__(*args)

	def db_insert_relations(self):
		col = self.collection
		col._insert_relation(self.id, self.linked_agendas, "Agenda_Agenda", "agenda1", "agenda2")

	@staticmethod
	def db_delete_relations(collection, id):
		collection._delete_relation(id, "Agenda_Agenda", "agenda1")
		collection._delete_relation(id, "Agenda_Agenda", "agenda2")

	def delete(self, owner):
		pass # TODO events
