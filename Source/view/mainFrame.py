import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from left import LeftBox


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Votre Agenda")
        self.add(LeftBox())


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
