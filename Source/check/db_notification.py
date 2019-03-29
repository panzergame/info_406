# -*- coding: utf-8 -*-

from core import *
from datetime import datetime
from db import *

import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="root", database="info_406")
cursor = conn.cursor()

collection = DbCollection(cursor)

account = Account.new(collection, set(), "jean", "root", "jean.michel@gmail.com")
jean = User.new(collection, "Jean", "Michel", "jean.michel@gmail.com", "00", None, account)

account.add_user(jean)

perso_agenda = Agenda.new(collection, "Personnel Tata", set(), set())
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

notif = Notification.new(collection, math104, perso_agenda)

collection.flush()

conn.commit()

cursor.close()
