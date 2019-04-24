# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
#from core import *
#from .group import *

class DefaultUserDeletionDialog(Gtk.Dialog):
	def __init__(self, parent):
		super().__init__("Suppression d'utilisateur(s)", parent, 0)

		label = Gtk.Label("""ATTENTION !
		
La suppression des utilisateurs sélectionnés entraînera la suppression 
de toutes les données les concernant (groupes, évènements, etc).
	
	Etes-vous sûr de vouloir procéder à la suppression ?
""")
		b_confirm = Gtk.Button(label="Valider", hexpand = True)
		#b_confirm.connect("clicked", self.on_confirm)
		b_cancel = Gtk.Button(label="Annuler", hexpand = True)
		#button.connect("clicked", self.on_cancel)
		button_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		label_box = Gtk.Box()
		label_box.set_border_width(15)

		box = self.get_content_area()
		label_box.add(label)
		box.add(label_box)
		button_box.add(b_confirm)
		button_box.add(b_cancel)
		box.add(button_box)
		self.show_all()

	#def on_confirm(self):

	#def on_cancel(self):

class AllUsersDeletionDialog(Gtk.Dialog):
	def __init__(self, parent):
		super().__init__("Suppression d'utilisateur(s)", parent, 0)

		label = Gtk.Label("""ATTENTION !
		
Vous êtes sur le point de supprimer tous les utilisateurs de ce compte.

La suppression des utilisateurs sélectionnés entraînera la suppression 
de toutes les données les concernant (groupes, évènements, etc).

		Etes-vous sûr de vouloir procéder à la suppression ?
	""")
		b_confirm = Gtk.Button(label="Valider", hexpand=True)
		# b_confirm.connect("clicked", self.on_confirm)
		b_cancel = Gtk.Button(label="Annuler", hexpand=True)
		# button.connect("clicked", self.on_cancel)
		button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		label_box = Gtk.Box()
		label_box.set_border_width(15)

		box = self.get_content_area()
		label_box.add(label)
		box.add(label_box)
		button_box.add(b_confirm)
		button_box.add(b_cancel)
		box.add(button_box)
		self.show_all()

d = AllUsersDeletionDialog(None)
d.run()
d.destroy()
Gtk.main()
