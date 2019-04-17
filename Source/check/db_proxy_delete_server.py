# -*- coding: utf-8 -*-

from server import *

import xmlrpc.client

from client import *
from core import *

s = xmlrpc.client.ServerProxy('http://localhost:8000', use_builtin_types=True)

collection = ServerClientCollection(s)

account = collection.load_account("root", "root")

for group in collection.load_groups("USMB"):

	print(group.subscribers)

	print(account.delete())

	print(group.subscribers)

	break

collection.flush()
