from .agenda import *

class User:
	def __init__(self, first_name, last_name, email, tel):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.tel = tel
		self.agenda = Agenda("Personnel")

	def __repr__(self):
		return "{} {}".format(self.first_name, self.last_name)
