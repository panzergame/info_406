from core import *
from datetime import date

class MyCollection(Collection):
	def __init__(self):
		super().__init__()
		
		self.id = 0

	def _new(self, data, type):
		print("[Collection] new", type.__name__, self.id)
		data.id = self.id
		self.id += 1

collection = MyCollection()

account = Account.new(collection, set(), "root", "root", "michel@gmail.com")
perso_agenda = Agenda.new(collection, "Personnel", set(), set())
work_agenda = Agenda.new(collection, "Travail", set(), set())
cheval_agenda = Agenda.new(collection, "Cheval", set(), set())

usmb = Group.new(collection, "USMB", set(), set(), {work_agenda}, set())
cheval = Group.new(collection, "Le cheval c'est trop génial !", set(), set(), set(), set())

toto = User.new(collection, "Toto", "Dupont", "toto@mail.com", "0656565656", perso_agenda, set())
tata = User.new(collection, "Tata", "Du…", "toto@mail.com", "0656565656", perso_agenda, set())

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

def add(ag, slot, type):
	event = Event.new(collection, slot, type, "", set(), set())
	ag.add_event(event)

# Création de 2 évenement ajouté sur chaque agenda
midi = Slot(date.today(), 12, 1.5)
soir = Slot(date.today(), 20, 3)
print(midi, soir)

add(perso_agenda, midi, "amis")
add(work_agenda, soir, "reunion")
add(cheval_agenda, midi, "manif")

state("Ajout d'evenements")

print(perso_agenda, perso_agenda.all_events)
print(work_agenda, work_agenda.all_events)
print(cheval_agenda, cheval_agenda.all_events)

cheval_agenda.remove_event(list(cheval_agenda.events)[0])

state("Suppression d'un evenement")

print(perso_agenda, perso_agenda.all_events)
print(work_agenda, work_agenda.all_events)
print(cheval_agenda, cheval_agenda.all_events)

account.delete()
