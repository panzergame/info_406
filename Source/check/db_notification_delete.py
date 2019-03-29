# -*- coding: utf-8 -*-

from core import *
from datetime import datetime
from db import *

import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="root", database="info_406")
cursor = conn.cursor()

collection = DbCollection(cursor)

group = Group.load(collection, 1)

account = Account.load(collection, 1)
user = list(account.users)[0]
agenda = user.agenda

print(agenda.notifications)

group.delete()

print(agenda.notifications)

collection.flush()

#conn.commit()

cursor.close()
