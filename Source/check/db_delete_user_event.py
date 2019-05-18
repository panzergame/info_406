# -*- coding: utf-8 -*-

from .db_open import *
from datetime import *

account = collection.load_account("root", "root")

user = list(account.users)[0]
agenda = user.agenda
event = list(agenda.all_events(datetime(2019, 5, 1), datetime(2019, 5, 2)))[0]

chunk = list(agenda._chunks.values())[0]

#for event in chunk:
	#print(event.id)

print("delete event", event.id)

event.delete()

#for event in chunk:
	#print(event.id)
print("delete agenda", event.id)
agenda.delete()

collection.flush()
