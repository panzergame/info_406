# -*- coding: utf-8 -*-

from core import *
from db import *
from datetime import datetime

import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="root", database="info_406")
cursor = conn.cursor()

collection = DbCollection(cursor)

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

#user.delete()

collection.flush()

#conn.commit()
cursor.close()
