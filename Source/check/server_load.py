# -*- coding: utf-8 -*-

from server import *

import xmlrpc.client

from client import *
from core import *

s = xmlrpc.client.ServerProxy('http://localhost:8000', use_builtin_types=True)

collection = ClientCollection(s)

account = collection.load_account("root", "root")
print("Account:", account)

user = User.new(collection, "toto", "michel", "michel@toto.com", "0000528258")

for user in account.users:
	print(user.first_name)
