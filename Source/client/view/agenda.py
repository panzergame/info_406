import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#######################################################################################################################

# Classe definissant un Agenda :

class Agenda(Gtk.Box):
    # On appelle le constructeur de la classe mère avec un agencement vertical et un espacement entre éléments
    # de 6 pixels :
    def __init__(self, name):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # On renseigne le nom de notre agenda :
        self.name = Gtk.Label(name, xalign=0)

        # On ajoute les éléments à notre boîte :
        self.pack_start(self.name, True, True, 0)