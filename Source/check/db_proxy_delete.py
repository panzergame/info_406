# -*- coding: utf-8 -*-

from .db_open import *

account = Account.load(collection, 1)
group = Group.load(collection, 1)

print(group.subscribers)

account.delete()

print(group.subscribers)

collection.flush()

#conn.commit()
cursor.close()
