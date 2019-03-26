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

print(group.subscribers)

account.delete()

print(group.subscribers)

collection.flush()

#conn.commit()
cursor.close()
