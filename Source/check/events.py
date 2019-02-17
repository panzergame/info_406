from core import *
from datetime import datetime

class MyCollection(Collection):
	def __init__(self):
		super().__init__()
		
		self.id = 0

	def _new(self, data, type):
		print("[Collection] new", type.__name__, self.id)
		data.id = self.id
		self.id += 1

	def _delete(self, data, type):
		print("[Collection] delete", type.__name__, data.id)

collection = MyCollection()

account = Account.new(collection, set(), "root", "root", "michel@gmail.com")
toto_agenda = Agenda.new(collection, "Personnel Toto", set(), set())
tata_agenda = Agenda.new(collection, "Personnel Tata", set(), set())
work_agenda = Agenda.new(collection, "Travail", set(), set())
cheval_agenda = Agenda.new(collection, "Cheval", set(), set())

usmb = Group.new(collection, "USMB", set(), set(), {work_agenda}, set())
cheval = Group.new(collection, "Le cheval c'est trop génial !", set(), set(), set(), set())

toto = User.new(collection, "Toto", "Dupont", "toto@mail.com", "0656565656", toto_agenda, set())
tata = User.new(collection, "Tata", "Du…", "toto@mail.com", "0656565656", tata_agenda, set())

def state(op):
	print("========== {} =========".format(op))
	print(account)
	print(usmb)
	print(cheval)
	print(toto)
	print(tata)

# Compte
account.add_user(toto)
account.add_user(tata)

state("Ajout de 2 utilisateurs :")
account.remove_user(tata)

state("Suppression de tata :")
account.add_user(tata)

# Groupe

usmb.subscribe(toto)
cheval.subscribe(toto)
cheval.subscribe(tata)

state("Ajout de membre :")

# Agenda

cheval.add_agenda(cheval_agenda)

state("Ajout d'un agenda :")

cheval.remove_agenda(cheval_agenda)

state("Suppression d'un agenda :")
cheval.add_agenda(cheval_agenda)

# Evenements

def add(ag, start, end, type):
	event = Event.new(collection, start, end, type, "", set(), set())
	ag.add_event(event)

# Création de 4 évenements ajoutés sur chaque agenda
add(toto_agenda, datetime(2019, 1, 15, 12), datetime(2019, 1, 15, 13), "amis")
add(tata_agenda, datetime(2019, 5, 15, 12), datetime(2019, 5, 15, 13), "teuufff")
add(work_agenda, datetime(2019, 10, 5, 20), datetime(2019, 10, 5, 23), "reunion")
add(cheval_agenda, datetime(2019, 12, 15, 12), datetime(2019, 12, 15, 13), "manif")

state("Ajout d'evenements")

print(toto_agenda, toto_agenda.all_events)
print(tata_agenda, tata_agenda.all_events)
print(work_agenda, work_agenda.all_events)
print(cheval_agenda, cheval_agenda.all_events)

manif = list(cheval_agenda.events)[0]
cheval_agenda.remove_event(manif)
manif.delete()

state("Suppression d'un evenement")

print(toto_agenda, toto_agenda.all_events)
print(tata_agenda, tata_agenda.all_events)
print(work_agenda, work_agenda.all_events)
print(cheval_agenda, cheval_agenda.all_events)

account.delete()
usmb.delete()
cheval.delete()
