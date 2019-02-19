# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from core import *
from .mainBox import MainBox
from client.model.common import *
from datetime import datetime

class MyWindow(Gtk.Window):

    def __init__(self, account, common):
        Gtk.Window.__init__(self, title="Votre Agenda")
        self.account = account
        self.common = common
        self.add(MainBox(account, common))

# DEMMOOOOOOO

collection = Collection()

ag = Agenda.new(collection, "Personnel", set(), set())
work_agenda = Agenda.new(collection, "Personnel", set(), set())
usmb_agenda = Agenda.new(collection, "L2-MIST", set(), set())
dessin_agenda = Agenda.new(collection, "Club Dessin", set(), set())

user = User.new(collection, "Toto", "Dupont", "toto@mail.com", "0656565656", ag, set())
usmb = Group.new(collection, "USMB", set(), set(), {usmb_agenda}, set())
dessin = Group.new(collection, "Club Dessin", set(), set(), {dessin_agenda}, set())
user2 = User.new(collection, "Loulou", "Martin", "loulou@mail.com", "0666666666", work_agenda, set())
usmb.subscribe(user2)
dessin.subscribe(user2)
account = Account.new(collection, {user}, "zut", "flute", user.email)
account.add_user(user2)

def add(ag, start, end, type, desc):
	event = Event.new(collection, start, end, type, desc, set(), set())
	ag.add_event(event)

for i in range(7):
	add(ag, datetime(2019, 2, 18 + i, 12), datetime(2019, 2, 18 + i, 13), "repas", "Repas avec les copains")
	add(usmb_agenda, datetime(2019, 2, 18 + i, 8), datetime(2019, 2, 18 + i, 18), "examen", "Examen de rattrapage")

common = Common()
common.day = datetime(2019, 2, 18)
common.event_clicked = list(ag.events)[0]

win = MyWindow(account, common)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
