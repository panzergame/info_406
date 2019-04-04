# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
from .db_open import *

michel_agenda = Agenda.new(collection, "Personnel", set(), set(), set())
didier_agenda = Agenda.new(collection, "Personnel", set(), set(), set())

michel = User.new(collection, "Michel", "Dupont", "michel.dupont@mail.com", "0656565656", None, set())
didier = User.new(collection, "Xavier", "Dupont", "didier.durand@mail.com", "0656565656", None, set())

michel.agenda = michel_agenda
didier.agenda = didier_agenda

account = Account.new(collection, set(),  "root", "root", "root@gmail.com")
account.add_user(michel)
account.add_user(didier)

usmb = Group.new(collection, "USMB", set(), set(), set(), set())

l2_agenda1 = Agenda.new(collection, "L2-INFO-1", set(), set(), set())
l2_agenda2 = Agenda.new(collection, "L2-INFO-2", set(), set(), set())
l2_agenda3 = Agenda.new(collection, "L2-INFO-3", set(), set(), set())
l2_agenda4 = Agenda.new(collection, "L2-INFO-4", set(), set(), set())

usmb.add_agenda(l2_agenda1)
usmb.add_agenda(l2_agenda2)
usmb.add_agenda(l2_agenda3)
usmb.add_agenda(l2_agenda4)

poney = Group.new(collection, "Aqua-poney", set(), set(), set(), set())
junior_agenda = Agenda.new(collection, "Junior", set(), set(), set())
expert_agenda = Agenda.new(collection, "Expert", set(), set(), set())

poney.add_agenda(junior_agenda)
poney.add_agenda(expert_agenda)


def add(ag, start, end, type):
	event = Event.new(collection, start, end, type, "", set(), set())
	ag.add_event(event)

add(junior_agenda, datetime(2019, 4, 7, 13), datetime(2019, 4, 7, 19), "Initiation")
add(l2_agenda1, datetime(2019, 4, 1, 13), datetime(2019, 4, 1, 14), "INFO_404")
add(l2_agenda1, datetime(2019, 4, 1, 15), datetime(2019, 4, 1, 17), "INFO_405")

collection.flush()
conn.commit()
cursor.close()
