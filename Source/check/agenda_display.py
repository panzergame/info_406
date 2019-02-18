import cairo
from datetime import *
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from Source.client.view import agenda


############ Classes de remplacement des entités ##################################
class tempAgenda():
    def __init__(self, events):
        self.all_events = events

class tempEvent():
    def __init__(self):
        #todo supprimer
        self.type="Manger"
        self.start=datetime(2019,1,2,8,0)
        self.end=datetime(2019,1,2,23,30)

class tempEvent2():
    def __init__(self):
        #todo supprimer
        self.type="Dormir"
        self.start=datetime(2019,1,3,12,0)
        self.end=datetime(2019,1,3,20,0)

class tempEvent3():
    def __init__(self):
        #todo supprimer
        self.type="Mourir"
        self.start=datetime(2019,1,6,6,0)
        self.end=datetime(2019,1,6,10,15)

################################# TESTS  ###########################################

agenda = tempAgenda([tempEvent(), tempEvent2(),tempEvent3()])

class MyWindow(Gtk.Window):
    def __init__(self):
            
        Gtk.Window.__init__(self, title="Hello World")
        self.add(AgendaBox(agenda, datetime(2019,1,1)))
        
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
