# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from core import *
from .main_box import MainBox
from client.model.common import Common
from datetime import datetime

from db import *

import mysql.connector

# Création de la collection.

conn = mysql.connector.connect(host="localhost", user="root", password="root", database="info_406_demo")
cursor = conn.cursor()
collection = DbCollection(cursor)

# Récupération du compte.
account = Account.load(collection, 1)

# Creéation de la session.
common = Common()
common.day = datetime(2019, 2, 18)
common.event_clicked = None
common.account = account

class MyWindow(Gtk.Window):

    def __init__(self, common):
        Gtk.Window.__init__(self, title="Votre Agenda")
        self.add(MainBox(common))

win = MyWindow(common)

win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
