# -*- coding: utf-8 -*-

from core import *
from .data import *

class DbAccount(Account, DbData):
	db_attr_names = ("login", "mdp", "email")
	db_table = "Account"

	def __init__(self, *args):
		super().__init__(*args)

	@classmethod
	def db_delete_proxies(cls, collection, _id):
		return collection._euthanasy_proxies(User, "account", _id)
