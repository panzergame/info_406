# -*- coding: utf-8 -*-

from core import *
from .data import *

class DbGroup(Group, DbData):
	db_attr_names = ("name", )
	db_table = "Group"

	def __init__(self, *args):
		super().__init__(*args)

	def db_insert_relations(self):
		col = self.collection
		col._insert_relation(self.id, self.admins, "Group_Admin", "group", "admin")
		col._insert_relation(self.id, self.subscribers, "Group_User", "group", "user")

	@staticmethod
	def db_delete_relations(collection, id):
		collection._delete_relation(id, "Group_Admin", "group")
		collection._delete_relation(id, "Group_User", "group")
