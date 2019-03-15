# -*- coding: utf-8 -*-

from core import *

class DbData:
	def db_new(self):
		self.collection._insert(self.db_table, self, self.db_attr_names)

	def db_update(self):
		self.collection._update(self.db_table, self, self.db_attr_names)

	def db_delete(self):
		self.collection._delete(self)

	def db_insert_relations(self):
		pass

	def db_delete_relations(self):
		pass
