# -*- coding: utf-8 -*-

from .db_open import *

account = collection.load_account("root", "root")

for group in collection.load_groups("USMB"):

	print(group.subscribers)

	print(account.delete())

	print(group.subscribers)

	break

collection.flush()

#conn.commit()
cursor.close()
