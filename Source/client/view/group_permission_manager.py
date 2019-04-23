# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from client.model import permission_manager_model

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
		inside.add(AdminSearchEntry())
		inside.add(AdminSearchResultsTree(manager_common.get_admin_search_results(""), manager_common))

		#Listes des membres et barre de recherche des membres
		inside.add(SubtitleFrame("Membres du groupe"))
		inside.add(MemberSearchEntry())
		inside.add(MemberSearchResultsTree(manager_common.get_member_search_results(""), manager_common))

		#Bouton de confrimation des changements
		inside.add(ApplyChangesButton())

		self.show_all()

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

class AdminSearchEntry(Gtk.SearchEntry):
	def __init__(self):
		Gtk.SearchEntry.__init__(self)

class MemberSearchEntry(Gtk.SearchEntry):
	def __init__(self):
		Gtk.SearchEntry.__init__(self)

class AdminSearchResultsTree(Gtk.Box):
	def __init__(self, admins, manager_common):
		Gtk.Box.__init__(self)

		self.manager_common = manager_common

		manager_common.add_observer(self)

		self.create_admin_list_tree_model(admins, manager_common)
		
		self.add_tree_view()

	def create_admin_list_tree_model(self, admins, manager_common):
		self.admin_list = Gtk.ListStore(str, str, object)
		for admin in admins:
			self.admin_list.append([admin.first_name,admin.last_name,PermissionCheckButton(admin in manager_common.admin_to_member, admin)])
	
	def add_tree_view(self):
		self.tree_view = Gtk.TreeView(model=self.admin_list)

		first_name_renderer = Gtk.CellRendererText()
		first_name_col=Gtk.TreeViewColumn("Prénom", first_name_renderer, text=0)
		first_name_col.set_expand(True)
		self.tree_view.append_column(first_name_col)

		last_name_renderer = Gtk.CellRendererText()
		last_name_col=Gtk.TreeViewColumn("Nom", last_name_renderer, text=0)
		last_name_col.set_expand(True)
		self.tree_view.append_column(last_name_col)

		toggle_renderer = Gtk.CellRendererToggle()
		toggle_col=Gtk.TreeViewColumn("Enlever les droits", toggle_renderer)
		toggle_col.set_expand(True)
		toggle_col.set_alignment(0.5)
		self.tree_view.append_column(toggle_col)

		self.add(self.tree_view)

		self.tree_view.set_property("expand","True")
		self.tree_view.get_selection().set_mode(Gtk.SelectionMode.NONE)

	def update(self, model):
		self.tree_view.delete()
		self.create_admin_list_tree_model(model.get_admin_search_results(model.admin_search))
		self.add_tree_view()
		self.show_all()


		

class MemberSearchResultsTree(Gtk.Box):
	def __init__(self, members, manager_common):
		Gtk.Box.__init__(self)

		self.manager_common = manager_common

		self.create_member_list_tree_model(members, manager_common)
		
		self.add_tree_view()

	def create_member_list_tree_model(self, members, manager_common):
		self.member_list = Gtk.ListStore(str, str, object)
		for member in members:
			self.member_list.append([member.first_name,member.last_name,PermissionCheckButton(member in manager_common.member_to_admin, member)])

	def add_tree_view(self):
		self.tree_view = Gtk.TreeView(model=self.member_list)

		first_name_renderer = Gtk.CellRendererText()
		first_name_col=Gtk.TreeViewColumn("Prénom", first_name_renderer, text=0)
		first_name_col.set_expand(True)
		self.tree_view.append_column(first_name_col)

		last_name_renderer = Gtk.CellRendererText()
		last_name_col=Gtk.TreeViewColumn("Nom", last_name_renderer, text=0)
		last_name_col.set_expand(True)
		self.tree_view.append_column(last_name_col)

		toggle_renderer = Gtk.CellRendererToggle()
		toggle_col=Gtk.TreeViewColumn("Ajouter les droits", toggle_renderer)
		toggle_col.set_expand(True)
		toggle_col.set_alignment(0.5)
		self.tree_view.append_column(toggle_col)

		self.add(self.tree_view)

		self.tree_view.set_property("expand","True")
		self.tree_view.get_selection().set_mode(Gtk.SelectionMode.NONE)

	def update(self, model):
		self.tree_view.delete()
		self.create_member_list_tree_model(model.get_member_search_results(model.member_search))
		self.add_tree_view()
		self.show_all()



class PermissionCheckButton(Gtk.CheckButton):
	def __init__(self, state, member):
		super().__init__()
		self.member = member
		self.set_active(state)

class ApplyChangesButton(Gtk.Button):
	def __init__(self, text="Confirmer"):
		Gtk.Button.__init__(self, label=text)
		self.set_halign(Gtk.Align.CENTER)

d = PermManagementDialog()
d.run()
Gtk.main()