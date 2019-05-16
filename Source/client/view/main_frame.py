# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk , Gdk

from .main_box import *

class MainFrame(Gtk.Window):
    def __init__(self, common):

        Gtk.Window.__init__(self, title="Votre Agenda")
        self.add(MainBox(common))
        self.set_name("MainFrame")
        #pour la démo:
        #self.fullscreen()



        #Initialisation d'un fichier CSS:
        """style_provider = Gtk.CssProvider()
        css = open('client/view/style.css' ,'rb')
        css_data = css.read()
        css.close()

        style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)"""
