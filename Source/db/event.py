# -*- coding: utf-8 -*-

from core import *
from .data import *

class DbEvent(Event, DbData):
	db_attr_names = ("start", "end", "type", "description", "agenda")
	db_table = "Event"

	def __init__(self, *args):
		super().__init__(*args)

	def db_insert_relations(self):
		col = self.collection
		col._insert_relation(self.id, self.resources, "Event_Resource", "event", "resource")
		col._insert_relation(self.id, self.users, "Event_User", "event", "user")

	def db_delete_relations(self):
		col = self.collection
		col._delete_relation(self.id, "Event_Resource", "event")
		col._delete_relation(self.id, "Event_User", "event")
