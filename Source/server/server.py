from core import *

class Server:
	def __init__(self):
		self.session_id = 0
		self.sessions = {}

	def _dispatch(self, method, params):
		if method == "connect":
			return self.connect(*params)

		self_id, *args = params

		data = Data.load(self_id, None)
		print(data)
		# Obtenir une ressource
		# Verifier les droits
		# Executer la modification ou lecture

		return 0

	def connect(self, user, password):
		if not user in self.sessions:
			id = self.sessions[user] = self.session_id
			self.session_id += 1
			return id

		return self.sessions[user]
