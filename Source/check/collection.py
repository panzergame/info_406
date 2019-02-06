from core import *

class MyCollection(Collection):
	def __init__(self):
		super().__init__()

	def _load(self, id, type):
		""" Charge une données selon son type et id. """
		print("Loading  #", id, "of type", type.__name__)
		if type == User:
			return User(id, "Toto", "Dupont", "toto@mail.com", "0656565656", DataProxy(1, Agenda, self))
		if type == Agenda:
			return Agenda(id, "Personnel")

	def sync(self):
		""" Enregistre toutes les données. """
		pass

collection = MyCollection()

user = collection.load(0, User)
print(user)
print(user.agenda)
print(user.agenda.events)
print(user.agenda)
