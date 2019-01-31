class Account:
	def __init__(self, login, mdp, email):
		self.users = []
		self.login = login
		self.mdp = mdp
		self.email = email

	def add_users(self, user):
		self.users.append(user)
