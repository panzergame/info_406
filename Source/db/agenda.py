# -*- coding: utf-8 -*-

from core import *
from .data import *

class DbAgenda(Agenda, DbData):
	db_attr_names = ("name", "group", "user")
	db_table = "Agenda"

	def __init__(self, *args):
		super().__init__(*args)

	def db_insert_relations(self):
		col = self.collection
		col._insert_relation(self.id, self.linked_agendas, "Agenda_Agenda", "agenda1", "agenda2")

	def db_delete_relations(self):
		col = self.collection
		col._delete_relation(self.id, "Agenda_Agenda", "agenda1")
		col._delete_relation(self.id, "Agenda_Agenda", "agenda2")
