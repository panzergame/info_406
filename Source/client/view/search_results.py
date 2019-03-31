# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SearchResultsBox(Gtk.Box):
	def __init__(self, common):
		Gtk.Box.__init__(self)
		self.common=common
		common.add_observer(self)
		#TODO meilleur accès à collection ?
		#TODO Empêcher la recherche vide ?
		results = common.account.collection.load_groups(common.current_search_text)
		#Boîte avec défilement, qui contiendra les résultats d'une recherche
		self.inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.inner_box.set_property("expand","true")
		scroll = Gtk.ScrolledWindow()
		scroll.add(self.inner_box)
		self.add(scroll)
		self.show_results(results)

	def show_results(self, results):
		for group in results:
			self.inner_box.add(SingleSearchResultFrame(self.common, group))

	def update(self, common):
		for child in self.inner_box.get_children():
			child.destroy()
		results = common.account.collection.load_groups(common.current_search_text)
		self.show_results(results)
		self.show_all()



class SingleSearchResultFrame(Gtk.Frame):
	def __init__(self, common, group):
		Gtk.Frame.__init__(self)
		#Contenu du du résultat de la recherche
		result_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		result_box.add(Gtk.Label(group.name))
		result_box.add(AllAgendasFromResultBox(common, group))
		self.add(result_box)

class AllAgendasFromResultBox(Gtk.Box):
	def __init__(self, common, group):
		Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
		self.set_homogeneous(True)
		for agenda in group.agendas:
			self.add(SingleAgendaFromResultBox(common, agenda))

class SingleAgendaFromResultBox(Gtk.Box):
	def __init__(self, common, agenda):
		Gtk.Box.__init__(self)

		#Boîte permettant de récupérer l'évènement de clic
		event_catcher = Gtk.EventBox()
		event_catcher.add(Gtk.Label(agenda.name))

		#Assemblement
		self.add(event_catcher)
		self.connect("button_press_event", self.update_main_view, agenda, common)
		
	def update_main_view(self, widget, clickEvent, agenda, common):
		common.agenda_displayed = agenda