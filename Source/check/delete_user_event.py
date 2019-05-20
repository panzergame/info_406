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

ev1 = Event.new(collection, today, today + hour, "INFO_402", "", set(), set())
ev2 = Event.new(collection, today + hour, today + hour * 2, "INFO_402", "", set(), set())

l = WeakRefSet()
l.add(ev1)
l.add(ev2)

print("list :")
print(l)

print("weak refs ev1")
print(ev1._weakrefs)
print("weak refs ev2")
print(ev2._weakrefs)

print("delete 2")
ev2.delete()
print("delete 1")
ev1.delete()

print("list :")
print(l)
