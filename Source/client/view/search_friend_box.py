# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import *

from .user_list import *

class SearchFriendBox(Gtk.VBox):
    def __init__(self, common):
        Gtk.VBox.__init__(self)
        self.common = common

        #Recherche d'un utilisateurs"
        self.entry = Gtk.SearchEntry()
        self.entry.connect("search_changed", self.on_search_changed)
        self.sub = self.entry.get_text()

        #Liste des utilisateurs
        self.list = UserList(self.common)
        recherche = Gtk.Label()
        recherche.set_markup("\n \n <big> Ajouter des contacts</big>")
        self.pack_start(recherche, False , False , False)
        self.pack_start(self.entry , False, False, False)
        self.add(self.list)

        #Bouton pour ajouter les Utilisateurs
        add_img = Gtk.Image()
        add_img.set_from_file("client/view/image/add.png")
        add_friend_button = Gtk.Button()
        add_friend_button.add(add_img)
        add_friend_button.connect("clicked", self. on_add_friend_clicked)

    def on_search_changed(self, widget):
        self.sub = self.entry.get_text()
        self.update()

    def update(self):
        users = self.common.collection.load_users(self.sub)
        self.list.set_users(users)

    def on_add_friend_clicked():
        #On récupère la liste des utilisateurs avec VRAI

        #On ajoute dans les demandes l'utilisateur actuel avec les autres utilisateurs

        #On renvoie la nouvelle liste.
        self.update()
