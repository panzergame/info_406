# -*- coding: utf-8 -*-

from .db_open import *

account = Account.new(collection, set(), "jean", "root", "jean.michel@gmail.com")
jean = User.new(collection, "Jean", "Michel", "jean.michel@gmail.com", "00", None, account)

account.add_user(jean)

perso_agenda = Agenda.new(collection, "Personnel Tata", set(), set(), datetime(2000, 1, 1))
l2_agenda = Agenda.new(collection, "L2-INFO", set(), set())

group = Group.new(collection, "USMB", set(), set(), set(), set())

jean.agenda = perso_agenda
group.add_agenda(l2_agenda)

perso_agenda.link_agenda(l2_agenda)

today = datetime.now()
hour = timedelta(hours=1)

math104 = Event.new(collection, today, today + hour, "MATH_104", "", set(), set())
cafe = Event.new(collection, today, today + hour, "Cafe", "", set(), set())

l2_agenda.add_event(math104)
perso_agenda.add_event(cafe)

perso_agenda.sync_notifications()
for agenda in perso_agenda.linked_agendas:
	print(agenda.events)

print(perso_agenda.notifications)

collection.flush()

conn.commit()

cursor.close()
