# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PermManagementDialog(Gtk.Dialog):
	"""Dialogue qui permet de modifier les permissions des membres d'un groupe"""
	def __init__(self):
		Gtk.Dialog.__init__(self)
		inside = self.get_content_area()
		inside.set_spacing(1)
		#Nom du groupe
		inside.add(GroupNameHeader())

		#Listes des admins et barre de recherche des admins
		inside.add(SubtitleFrame("Administrateurs"))
		inside.add(AdminSearchEntry())
		inside.add(AdminSearchResultsTree("TODO admins liste"))

		#Listes des membres et barre de recherche des membres
		inside.add(SubtitleFrame("Membres du groupe"))
		inside.add(MemberSearchEntry())
		inside.add(MemberSearchResultsTree("TODO members liste"))

		#Bouton de confrimation des changements
		inside.add(ApplyChangesButton())

		self.show_all()

class GroupNameHeader(Gtk.HeaderBar):
	"""Sert à afficher le nom du groupe et son propriétaire dans un dialogue de gestion des permissions d'un gorupe"""
	def __init__(self, group_name="NomDuGroupe", owner_name="Dupont Jean"):
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
	def __init__(self, admins):
		Gtk.Box.__init__(self)

		self.admin_list = Gtk.ListStore(str, str, object)
		self.admin_list.append(["Francois","Marie",PermissionCheckButton(True, "admin")])
		self.admin_list.append(["AAA","BBB",PermissionCheckButton(True, "admin")])
		self.admin_list.append(["Marie","Francoise",PermissionCheckButton(True, "admin")])
		self.admin_list.append(["Jean","Paul",PermissionCheckButton(True, "admin")])

		self.tree_view = Gtk.TreeView(model=self.admin_list)
		

		c1_render = Gtk.CellRendererText()
		c1=Gtk.TreeViewColumn("Prénom", c1_render, text=0)
		c1.set_expand(True)
		self.tree_view.append_column(c1)

		c2_render = Gtk.CellRendererText()
		c2=Gtk.TreeViewColumn("Nom", c2_render, text=0)
		c2.set_expand(True)
		self.tree_view.append_column(c2)

		c3_render = Gtk.CellRendererToggle()
		c3=Gtk.TreeViewColumn("Enlever les droits", c3_render)
		c3.set_expand(True)
		c3.set_alignment(0.5)
		self.tree_view.append_column(c3)

		self.add(self.tree_view)
		self.tree_view.set_property("expand","True")
		self.tree_view.get_selection().set_mode(Gtk.SelectionMode.NONE)

class MemberSearchResultsTree(Gtk.Box):
	def __init__(self, members):
		Gtk.Box.__init__(self)

		self.member_list = Gtk.ListStore(str, str, object)
		self.member_list.append(["Paul","Deprès",PermissionCheckButton(True, "member")])
		self.member_list.append(["Jacques","Deloin",PermissionCheckButton(True, "member")])
		self.member_list.append(["Alain","Dupuis",PermissionCheckButton(True, "member")])

		self.tree_view = Gtk.TreeView(model=self.member_list)

		c1_render = Gtk.CellRendererText()
		c1=Gtk.TreeViewColumn("Prénom", c1_render, text=0)
		c1.set_expand(True)
		self.tree_view.append_column(c1)

		c2_render = Gtk.CellRendererText()
		c2=Gtk.TreeViewColumn("Nom", c2_render, text=0)
		c2.set_expand(True)
		self.tree_view.append_column(c2)

		c3_render = Gtk.CellRendererToggle()
		c3=Gtk.TreeViewColumn("Ajouter les droits", c3_render)
		c3.set_expand(True)
		c3.set_alignment(0.5)
		self.tree_view.append_column(c3)

		self.add(self.tree_view)
		self.tree_view.set_property("expand","True")
		self.tree_view.get_selection().set_mode(Gtk.SelectionMode.NONE)

class PermissionCheckButton(Gtk.CheckButton):
	def __init__(self, state, member):
		super().__init__()

class ApplyChangesButton(Gtk.Button):
	def __init__(self, text="Confirmer"):
		Gtk.Button.__init__(self, label=text)
		#self.set_hexpand(False)
		self.set_halign(Gtk.Align.CENTER)

d = PermManagementDialog()
d.run()
Gtk.main()