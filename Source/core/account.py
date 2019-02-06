from .data import *

class Account(Data):
	def __init__(self, id, users, login, mdp, email):
		super().__init__(id)

		self.users = users
		self.login = login
		self.mdp = mdp
		self.email = email

	def add_users(self, user):
		self.users.append(user)
