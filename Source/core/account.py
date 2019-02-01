from .data import *

class Account(Data):
	def __init__(self, login, mdp, email):
		super().__init__()

		self.users = []
		self.login = login
		self.mdp = mdp
		self.email = email

	def add_users(self, user):
		self.users.append(user)
