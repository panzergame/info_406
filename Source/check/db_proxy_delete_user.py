# -*- coding: utf-8 -*-

from .db_open import *

account = collection.load_account("root", "root")

for user in account.users:
	for group in user.groups:
		print(group.name)

for user in account.users:
	user.delete()
	break

collection.flush()
