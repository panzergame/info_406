# -*- coding: utf-8 -*-

from core import *
from datetime import datetime

class MyCollection(Collection):
	def __init__(self):
		super().__init__()
		
		self.id = 0

	def new(self, type, *args):
		data = type(self.id, self, *args)
		print("[Collection] new", type.__name__, self.id)
		self.id += 1
		return data

	def load_batched(self, _id, _type, *args):
		return set()

	def delete(self, data):
		print("[Collection] delete", type(data).__name__, data.id)

collection = MyCollection()

agenda = Agenda.new(collection, "Personnel Tata", set())

today = datetime.now()
hour = timedelta(hours=1)
ev = Event.new(collection, today, today + hour, "", "", set(), set())

agenda.add_event(ev)

notif = Notification.new(collection, ev)
ev.delete()
