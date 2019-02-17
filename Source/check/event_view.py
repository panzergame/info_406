from datetime import date
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from core import *
from client.view import *

class TestWindow(Gtk.Window):
#Fenêtre principale   
    def __init__(self, event):
        Gtk.Window.__init__(self, title="Test widget event")
        self.connect("destroy", Gtk.main_quit)

        #Ajout d'une boîte qui affiche l'evenement passé en parametre
        w = EventBox(event)
        self.add(w)

    def on_button_clicked(self, widget):
        print("Hello World")

class MyCollection(Collection):
	def __init__(self):
		super().__init__()
		
		self.id = 0

	def _new(self, data, type):
		data.id = self.id
		self.id += 1

def long_text(n):
#Pour créer automatiquement un texte volumineux
    text=""
    for i in range(n):
        text+="{} ".format(i)
    return text

collection = MyCollection()

#Horaire de test
test_slot = Slot(date.today(), 10, 12)

#Resources utilisées par l'evenement de test
r1 = Resource.new(collection,"chaises","B24",10)
r2 = Resource.new(collection, "crayon","B25",1)
r3 = Resource.new(collection,"tables","B28",20)
resources = set([r1,r2,r3])

#Utilisateurs participant à l'event
ag = Agenda.new(collection, "Personnel", set(), set())
u1 = User.new(collection, "Jean", "Dupont", "jeandup@slt.com", "0622558877", ag)
u2 = User.new(collection, "Georges", "Lucas", "jeandup@slt.com", "0622558877", ag)
u3 = User.new(collection, "Serges", "Pailette", "jeandup@slt.com", "0622558877", ag)
users = set([u1,u2,u3])

#Creation de l'evenement
test_event = Event.new(collection, test_slot, "Type",long_text(400), resources, users)

win = TestWindow(test_event)
win.show_all()
Gtk.main()
