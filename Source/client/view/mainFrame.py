import gi

from Source.check import events

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Source.core import *
from left import LeftBox


class MyWindow(Gtk.Window):

    def __init__(self, account):
        Gtk.Window.__init__(self, title="Votre Agenda")
        self.account = account
        self.add(LeftBox(account))


collection = events.MyCollection()

ag = Agenda.new(collection, "Personnel", set(), set())
work_agenda = Agenda.new(collection, "Travail", set(), set())

user = User.new(collection, "Toto", "Dupont", "toto@mail.com", "0656565656", ag)
user2 = User.new(collection, "Loulou", "Martin", "loulou@mail.com", "0666666666", work_agenda)
account = Account.new(collection, [user], "zut", "flute", user.email)
account.add_users(user2)

win = MyWindow(account)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
