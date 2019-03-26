# -*- coding: utf-8 -*-

from core import *
from .data import *

class DbEvent(Event, DbData):
	db_attr_names = ("start", "end", "type", "description", "agenda", "creation_date")
	db_table = "Event"

	def __init__(self, *args):
		super().__init__(*args)

	def db_insert_relations(self):
		col = self.collection
		col._insert_relation(self.id, self.resources, "Event_Resource", "event", "resource")
		col._insert_relation(self.id, self.users, "Event_User", "event", "user")

	@staticmethod
	def db_delete_relations(collection, id):
		collection._delete_relation(id, "Event_Resource", "event")
		collection._delete_relation(id, "Event_User", "event")
