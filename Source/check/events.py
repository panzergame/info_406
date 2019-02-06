from core import *
from datetime import date

user = User("Toto", "Dupont", "toto@mail.com", "0656565656")

# Utilisation de 2 agendas
ag = user.agenda
work_agenda = Agenda("Travail")

def add(ag, slot):
	ag.create_event(slot, "travail", "Reunion")

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
