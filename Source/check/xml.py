# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
from server import *
from core import *

class MyCollection(Collection):
	def __init__(self):
		super().__init__()
		
		self.id = 0

	def new(self, type, *args):
		data = type(self.id, self, *args)
		print("[Collection] new", type.__name__, self.id)
		self.id += 1
		return data

	def load_batched(self, _id, _type, *args):
		return set()

	def delete(self, data):
		print("[Collection] delete", type(data).__name__, data.id)

collection = MyCollection()

user = User.new(collection, "Jean", "Michel", "", "", None, set())
user.agenda = Agenda.new(collection, "Perso", set(), set(), set())
account = Account.new(collection, set(),  "root", "root", "root@gmail.com")
account.add_user(user)

converter = XMLConverter(collection)

xml = converter.to_xml(account)
print(xml)

data = converter.to_data(Account, xml)
print(data)

"""collection.flush()
conn.commit()
cursor.close()"""
