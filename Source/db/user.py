# -*- coding: utf-8 -*-

from core import *
from .data import *

class DbUser(User, DbData):
	db_attr_names = ("first_name", "last_name", "email", "tel", "account")
	db_table = "User"

	def __init__(self, *args):
		super().__init__(*args)

	@classmethod
	def db_delete_proxies(cls, collection, _id):
		from .agenda import DbAgenda
		return collection._euthanasy_proxies(DbAgenda, "user", _id)
