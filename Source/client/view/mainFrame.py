import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *


from left import LeftBox


class MyWindow(Gtk.Window):

    def __init__(self, account):
        Gtk.Window.__init__(self, title="Votre Agenda")
        this.account = account
        self.add(LeftBox(account))


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
