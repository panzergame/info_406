# -*- coding: utf-8 -*-

from .db_open import *

account = Account.load(collection, 1)
print(account.users)

account.delete()

collection.flush()

#conn.commit()
cursor.close()
