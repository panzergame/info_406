# -*- coding: utf-8 -*-

from core import *
from db import *
from datetime import datetime

import mysql.connector 

conn = mysql.connector.connect(host="localhost", user="root", password="root", database="info_406")
cursor = conn.cursor()

collection = DbCollection(cursor)

account = Account.load(collection, 1)
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

cursor.close()
