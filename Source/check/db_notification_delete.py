# -*- coding: utf-8 -*-

from .db_open import *

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
