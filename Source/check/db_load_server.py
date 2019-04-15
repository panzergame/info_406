# -*- coding: utf-8 -*-

from server import *

import xmlrpc.client

from client import *
from core import *

s = xmlrpc.client.ServerProxy('http://localhost:8000', use_builtin_types=True)

collection = ClientCollection(s)

account = collection.load_account("root", "root")
print("Account:", account)

def print_period(agenda, from_date, to_date):
	events = sorted(agenda.all_events(from_date, to_date), key=lambda x: x.start)
	print("Agenda:", agenda)
	print("Events between {} and {}".format(from_date, to_date))
	for event in events:
		print(event.start, event.end)

for user in account.users:
	ag = user.agenda
	print("User:", user)

	print_period(ag, datetime(2019, 1, 1, 12), datetime(2019, 2, 11, 0, 0))
	print_period(ag, datetime(2019, 1, 15, 12), datetime(2019, 1, 18, 0, 0))

	for group in user.groups:
		print("Group:", group.name)

groups = collection.load_groups("SMB")
print(groups)

collection.flush()
