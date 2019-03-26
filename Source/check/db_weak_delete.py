# -*- coding: utf-8 -*-

from core import *
from db import *
from datetime import datetime, timedelta

import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="root", database="info_406")
cursor = conn.cursor()

collection = DbCollection(cursor)

account = Account.load(collection, 1)
group = Group.load(collection, 1)

print("Liste d'utilisateurs:")
print("Group :", group.subscribers)
print("Account :", account.users)

print()
for user in set(group.subscribers):
	print("Suppression de", user)
	user.delete()

print()
print("Liste d'utilisateurs:")
print("Group :", group.subscribers)
print("Account :", account.users)

"""user = list(account.users)[0]
for group in user.groups:
	print(group.subscribers)

user.delete()

for group in user.groups:
	print(group.subscribers)
"""
collection.flush()

#conn.commit()
cursor.close()
