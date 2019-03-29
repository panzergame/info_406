
import persistent

class Account(persistent.Persistent):
	def __init__(self, user):
		print("init")
		self.balance = 0.0
		self.user = persistent.wref.WeakRef(user)

	def deposit(self, amount):
		self.balance += amount

	def cash(self, amount):
		assert amount < self.balance
		self.balance -= amount

class User(persistent.Persistent):
	def __init__(self):
		print("user init")

	

import ZODB, ZODB.FileStorage, BTrees.OOBTree, transaction

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

def write():
	user = User()
	root.accounts = BTrees.OOBTree.BTree()
	root.accounts['account-1'] = Account(user)
	root.user = user
	root.user2 = persistent.wref.WeakRef(user)


#write()
for ac in root.accounts:
	print(root.accounts[ac].user)
	del root.user
	#transaction.commit()
	print(root.accounts[ac].user)
