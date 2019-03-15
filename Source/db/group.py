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

	def db_delete_relations(self):
		col = self.collection
		col._delete_relation(self.id, "Group_Admin", "group")
		col._delete_relation(self.id, "Group_User", "group")
