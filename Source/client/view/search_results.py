# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SearchResultsBox(Gtk.Box):
	def __init__(self, common):
		Gtk.Box.__init__(self)
		self.common=common

		#TODO meilleur accès à collection ?
		results = common.account.collection.load_groups(common.current_search_text)
		print(results)

		#Boîte avec défilement, qui contiendra les résultats d'une recherche
		self.inner_box = Gtk.Box()
		scroll = Gtk.ScrolledWindow()
		scroll.add(self.inner_box)
		self.add(scroll)
		self.show_results(results)

	def show_results(self, results):
		for group in results:
			self.inner_box.add(SingleSearchResultBox(self.common, group))

	def update(self, results):
		for child in self.inner_box.get_children():
			child.destroy()
		self.show_results(results)



class SingleSearchResultBox(Gtk.Box):
	def __init__(self, common, group):
		Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
		self.add(Gtk.Label(group.name))
		self.add(SelectGroupButton(common, group))

class SelectGroupButton(Gtk.Button):

	def __init__(self, common, group):
		Gtk.Button.__init__(self, label="Rechercher")
		self.group=group
		self.common=common
		self.connect("clicked", self.update_common)
	
	def update_common(self):
		print("slt !!!")
