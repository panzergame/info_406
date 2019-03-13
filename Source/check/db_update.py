# -*- coding: utf-8 -*-

from core import *
from db import *
from datetime import datetime

import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="root", database="info_406")
cursor = conn.cursor()

collection = DbCollection(cursor)

account = Account.load(collection, 1)
print(account.users)
for user in account.users:
	print(user.account)
	user.email = "TOTO@gmail.com"
	print(user.email, id(user))

	user.update()

user = list(account.users)[0]
account.remove_user(user)
user.delete()

account.update()

collection.flush()

#conn.commit()
cursor.close()
