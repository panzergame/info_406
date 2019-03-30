# -*- coding: utf-8 -*-

from datetime import timedelta
from .db_open import *

account = Account.load(collection, 1)
for user in account.users:
	user.email = "TOTO@gmail.com"

user = list(account.users)[0]
user2 = list(account.users)[1]
account.remove_user(user)

group = list(user.groups)[0]
group.unsubscribe(user)

group2 = list(user2.groups)[0]
group2.unsubscribe(user2)

today = datetime.now()
hour = timedelta(hours=1)
day = timedelta(days=1)

start = today.replace(hour=0, minute=0)
end = today + day

agenda = user.agenda
print(agenda.all_events(start, end))

events = []
for i in range(4):
	ev = Event.new(collection, today + i * hour, today + (i + 1) * hour, "", "", set(), set())
	events.append(ev)
	agenda.add_event(ev)

print("Events ", start, end)
print(agenda.all_events(start, end))

for i in range(2):
	ev = events[i]
	agenda.remove_event(ev)
	ev.delete()

print(agenda.all_events(start, end))

user.delete()

collection.flush()

#conn.commit()
cursor.close()
