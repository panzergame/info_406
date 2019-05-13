# -*- coding: utf-8 -*-

from .data import *
from .dataproperty import *

class LinkedAgenda(WeakRefered):
	agenda = DataOwnerProperty("agenda")

	def __init__(self, agenda, last_sync=None):
		super().__init__()

		self._agenda = DataOwnerProperty.init(agenda, self)
		self.last_sync = last_sync

	def update(self):
		raise ValueError();
