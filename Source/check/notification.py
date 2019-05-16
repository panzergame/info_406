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

agenda = Agenda.new(collection, "Personnel Tata", set())
travail = Agenda.new(collection, "Travail", set())

def update():
	agenda.sync_notifications()
	print(agenda.notifications)

today = datetime.now()
hour = timedelta(hours=1)
half = timedelta(minutes=30)


ev = Event.new(collection, today, today + hour, "INFO_402", "", set(), set())
ev2 = Event.new(collection, today + hour + half, today + hour * 2 + half, "INFO_406", "", set(), set())
ev3 = Event.new(collection, today + hour, today +  hour * 2, "Amis", "", set(), set())

# ev2 et ev3 en collision

print(ev.intersect(ev))
print(ev.intersect(ev2), ev2.intersect(ev3))

travail.add_event(ev)
travail.add_event(ev2)

agenda.add_event(ev3)
agenda.link_agenda(travail)

update()

ev.delete()

print(travail.all_events(today, today + hour * 24))

update()

for notif in agenda.notifications:
	notif.status = Notification.ACCEPTED

print(agenda.notifications)

ev2.type = "cour"

update()
