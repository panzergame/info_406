from core import *
from db import *
from datetime import datetime

import mysql.connector 

conn = mysql.connector.connect(host="localhost", user="root", password="root", database="info_406")
cursor = conn.cursor()

collection = DbCollection(cursor)

account = Account.load(collection, 1)
print("Account:", account)

for user in account.users:
	ag = user.agenda
	print("User:", user)
	events = ag.all_events
	print("Agenda:", ag)
	for event in events:
		print("Event:", event.start, event.end)

	for group in user.groups:
		print("Group:", group.name)

cursor.close()
