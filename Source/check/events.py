from core import *
from datetime import date

class MyCollection(Collection):
	def __init__(self):
		super().__init__()
		
		self.id = 0

	def _new(self, data, type):
		print("new", type.__name__, self.id)
		data.id = self.id
		self.id += 1

collection = MyCollection()

ag = Agenda.new(collection, "Personnel", set(), set())
work_agenda = Agenda.new(collection, "Travail", set(), set())

user = User.new(collection, "Toto", "Dupont", "toto@mail.com", "0656565656", ag)

# Utilisation de 2 agendas

def add(ag, slot):
	ag.create_event(slot, "travail", "Reunion", set(), set())

# Création de 2 évenement ajouté sur chaque agenda
midi = Slot(date.today(), 12, 1.5)
soir = Slot(date.today(), 20, 3)
print(midi, soir)

add(ag, midi)
add(work_agenda, soir)

# Liaison agenda travail vers agenda perso
ag.link_agenda(work_agenda)

print(ag.events)
print(work_agenda.events)
# Doit afficher les deux évenements
print(ag.all_events)
