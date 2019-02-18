# -*- coding: utf-8 -*-

import gi

from check import events

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *
from .mainBox import MainBox
from client.model.common import *


class MyWindow(Gtk.Window):

    def __init__(self, account, common):
        Gtk.Window.__init__(self, title="Votre Agenda")
        self.account = account
        self.common = common
        self.add(MainBox(account, common))


collection = events.MyCollection()

ag = Agenda.new(collection, "Personnel", set(), set())
work_agenda = Agenda.new(collection, "Travail", set(), set())

user = User.new(collection, "Toto", "Dupont", "toto@mail.com", "0656565656", ag, set())
usmb = Group.new(collection, "USMB", set(), set(), {work_agenda}, set())
user2 = User.new(collection, "Loulou", "Martin", "loulou@mail.com", "0666666666", work_agenda, set())
usmb.subscribe(user2)
account = Account.new(collection, {user}, "zut", "flute", user.email)
account.add_user(user2)

common = Common()
win = MyWindow(account, common)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
