from core import *

# 0 : User
# 1 : Agenda

class MyCollection(Collection):
	def __init__(self):
		super().__init__()

	def _load(self, _id, type):
		""" Charge une données selon son type et id. """
		print("Loading  #", _id, "of type", type.__name__)
		if type == User:
			return User(_id, "Toto", "Dupont", "toto@mail.com", "0656565656", DataProxy(1, Agenda, self))
		if type == Agenda:
			return Agenda(_id, "Personnel")

	def sync(self):
		""" Enregistre toutes les données. """
		pass


if __name__ == "__main__":
	collection = MyCollection()

	user = collection.load(0, User)
	print(user)
	print(user.agenda)
	print(user.agenda.events)
	print(user.agenda.all_events)
	print(user.agenda)
