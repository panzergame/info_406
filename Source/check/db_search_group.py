# -*- coding: utf-8 -*-

from .db_open import *

account = collection.load_account("root", "root")

group = Group.new(collection, "Test")

for group in collection.load_groups("Test"):
	print(group)

collection.flush()

#conn.commit()
cursor.close()
