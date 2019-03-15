# -*- coding: utf-8 -*-

from core import *
from .data import *

class DbResource(Resource, DbData):
	db_attr_names = ("name", "location", "capacity", "group")
	db_table = "Resource"

	def __init__(self, *args):
		super().__init__(*args)
