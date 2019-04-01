# -*- coding: utf-8 -*-

from core import *
from .data import *

class DbNotification(Notification, DbData):
	db_attr_names = ("event", "agenda", "status")
	db_table = "Notification"

	def __init__(self, *args):
		super().__init__(*args)
