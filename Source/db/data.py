# -*- coding: utf-8 -*-

from core import *

class DbData:
	def db_new(self):
		self.collection._insert(self.db_table, self, self.db_attr_names)

	def db_update(self):
		self.collection._update(self.db_table, self, self.db_attr_names)

	@classmethod
	def db_delete(cls, collection, _id):
		collection._delete(cls.db_table, _id)

	def db_insert_relations(self):
		pass

	@staticmethod
	def db_delete_relations(collection, id):
		pass
