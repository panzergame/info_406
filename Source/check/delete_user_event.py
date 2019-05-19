# -*- coding: utf-8 -*-

from core import *
from datetime import datetime

class MyCollection(Collection):
	def __init__(self):
		super().__init__()

	def load_batched(self, _id, _type, *args):
		return set()

	def load_events(self, agenda, from_date, to_date):
		return set()

	def load_last_events(self, agenda, from_date, to_date):
		return set()

collection = MyCollection()

agenda = Agenda.new(collection, "perso")

today = datetime.now()
hour = timedelta(hours=1)
half = timedelta(minutes=30)

ev = Event.new(collection, today, today + hour, "INFO_402", "", set(), set())

agenda.add_event(ev)


print("delete", ev.id)
print(agenda._weakrefs)
print(ev._weakrefs)
ev.delete()

agenda.delete()
