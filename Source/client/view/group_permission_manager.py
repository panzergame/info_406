# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from client.model.permission_manager_model import *

class PermManagementDialog(Gtk.Dialog):
	"""Dialogue qui permet de modifier les permissions des membres d'un groupe"""
	def __init__(self, group):
		Gtk.Dialog.__init__(self)

		self.manager_common =  PermissionManagerModel(group.collection, group)

		inside = self.get_content_area()
		inside.set_spacing(1)
		#Nom du groupe
		inside.add(GroupNameHeader(group.name))

		#Listes des admins et barre de recherche des admins
		inside.add(SubtitleFrame("Administrateurs"))
		inside.add(AdminSearchEntry(self.manager_common))
		inside.add(AdminSearchResultsTrees(self.manager_common))

		#Listes des membres et barre de recherche des membres
		inside.add(SubtitleFrame("Membres du groupe"))
		inside.add(MemberSearchEntry(self.manager_common))
		inside.add(MemberSearchResultsTrees(self.manager_common))

		#Bouton de confrimation des changements
		inside.add(ApplyChangesButton(self))
		self.show_all()

	def confirm_changes(self, widget):
		self.manager_common.apply_changes()
		self.destroy()

class GroupNameHeader(Gtk.HeaderBar):
	"""Sert à afficher le nom du groupe et son propriétaire dans un dialogue de gestion des permissions d'un gorupe"""
	def __init__(self, group_name, owner_name="nom_proprio"):
		Gtk.HeaderBar.__init__(self)
		self.set_title(group_name)
		self.set_subtitle("créé par {}".format(owner_name))

class SubtitleFrame(Gtk.Frame):
	"""Sert à signaler une sous partie dans un dialogue de gestion des permissions d'un groupe"""
	def __init__(self, text):
		Gtk.Frame.__init__(self)
		#container (cadre)
		box = Gtk.Box(halign=Gtk.Align.CENTER)
		box.set_border_width(5)

		#label, titre de la sous partie
		label = Gtk.Label()
		label.set_markup("<b>{}</b>".format(text))

		#assemblage
		box.add(label)
		self.add(box)

class SearchResults(Gtk.Box):
	def __init__(self, manager_common, origin_set, new_set,toggle_permission_column_title):
		#origin_set est le set de membres dont on veut changer une propriété
		#new_set est le set dans lequel les membres se trouvent quand on a changé la propriété
		super().__init__()
		self.manager_common = manager_common
		self.origin_set = origin_set
		self.new_set = new_set
		self.toggle_permission_column_title = toggle_permission_column_title

		self.models_list = {}
		self.tree_view_list = {}

		self.origin_set_id = "origin_set"
		self.new_set_id = "new_set"

		self.create_tree_model(self.origin_set_id)
		self.add_tree_view(self.origin_set_id)
		self.create_tree_model(self.new_set_id)
		self.add_tree_view(self.new_set_id)
		

	def create_tree_model(self, id):
		#Crée le modèle de la liste
		self.models_list[id] = Gtk.ListStore(str, str, bool, object)
		#Nom membre, prénom membre, si ses permission changent ou non, objet membre
		self.update_tree_model(id)

	def update_tree_model(self, id):
		self.models_list[id].clear()

		if id==self.origin_set_id:
			for member in (self.origin_set - self.new_set):
				#Set des membres résultats de la recherche qui n'ont pas déjà été sélectionnés
				self.models_list[id].append([member.first_name,member.last_name,False,member])
		elif id==self.new_set_id:
			for member in self.new_set:
				self.models_list[id].append([member.first_name,member.last_name,True,member])
		else:
			pass
			#Id(de modèle d'arbre) donnée inexistante

	def update_all_tree_models(self):
		for model_id in self.models_list:
			self.update_tree_model(model_id)

	def add_tree_view(self, model_id):
		#Crée la vue de la liste
		self.tree_view_list[model_id] = Gtk.TreeView(model=self.models_list[model_id])
		tree_model = self.models_list[model_id]
		tree_view = self.tree_view_list[model_id]

		#Colonne prénom
		first_name_renderer = Gtk.CellRendererText()
		first_name_col=Gtk.TreeViewColumn("Prénom", first_name_renderer, text=0)
		first_name_col.set_expand(True)
		tree_view.append_column(first_name_col)

		#Colonne nom
		last_name_renderer = Gtk.CellRendererText()
		last_name_col=Gtk.TreeViewColumn("Nom", last_name_renderer, text=1)
		last_name_col.set_expand(True)
		tree_view.append_column(last_name_col)

		#Colonne contenant la case à cocher pour changer les permissions
		toggle_renderer = Gtk.CellRendererToggle()
		toggle_col=Gtk.TreeViewColumn(self.toggle_permission_column_title, toggle_renderer, active=2)
		toggle_col.set_expand(True)
		toggle_col.set_alignment(0.5)
		tree_view.append_column(toggle_col)

		#Propriétés d'affichage
		tree_view.set_property("expand","True")
		tree_view.get_selection().set_mode(Gtk.SelectionMode.NONE)

		toggle_renderer.connect("toggled", self.on_clicked, model_id)

		self.add(tree_view)

	def on_clicked(self, widget, path, model_id):
		row_clicked = self.models_list[model_id][path]
		if model_id==self.new_set_id:
			self.new_set.discard(row_clicked[3])
			self.origin_set.add(row_clicked[3])
		else:
			self.new_set.add(row_clicked[3])
			self.origin_set.discard(row_clicked[3])
			
		#Mis à jour de la recherche après avoir cliqué
		self.update_search_results(self.origin_set)


	def update_search_results(self, new_results_set):
		self.origin_set = new_results_set
		self.update_all_tree_models()
		self.show_all()

class AdminSearchEntry(Gtk.SearchEntry):
	def __init__(self, manager_common):
		Gtk.SearchEntry.__init__(self)
		self.manager_common = manager_common
		self.connect("search-changed", self.on_search_changed)
	
	def on_search_changed(self, widget):
		self.manager_common.admin_search = self.get_text()

class MemberSearchEntry(Gtk.SearchEntry):
	def __init__(self, manager_common):
		Gtk.SearchEntry.__init__(self)
		self.manager_common = manager_common
		self.connect("search-changed", self.on_search_changed)
	
	def on_search_changed(self, widget):
		self.manager_common.member_search = self.get_text()

class AdminSearchResultsTrees(SearchResults):
	def __init__(self, manager_common):
		super().__init__(manager_common, manager_common.get_admin_search_results(), manager_common.admin_to_member, "Enlever les droits")
	
	def update(self, manager_common):
		self.update_search_results(manager_common.get_admin_search_results())

class MemberSearchResultsTrees(SearchResults):
	def __init__(self, manager_common):
		super().__init__(manager_common, manager_common.get_member_search_results(), manager_common.member_to_admin, "Ajouter les droits")
		manager_common.add_observer(self)
	
	def update(self, manager_common):
		self.update_search_results(manager_common.get_member_search_results())

class PermissionCheckButton(Gtk.CheckButton):
	def __init__(self, state, member):
		super().__init__()
		self.member = member
		self.set_active(state)

class ApplyChangesButton(Gtk.Button):
	def __init__(self, parent_dialog, text="Confirmer"):
		Gtk.Button.__init__(self, label=text)
		self.set_halign(Gtk.Align.CENTER)
		self.connect("clicked", parent_dialog.confirm_changes)

