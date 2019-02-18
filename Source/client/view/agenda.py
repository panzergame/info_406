import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#######################################################################################################################

# Classe definissant un Agenda :

class Agenda(Gtk.Box):
    # On appelle le constructeur de la classe mère avec un agencement vertical et un espacement entre éléments
    # de 6 pixels :
    def __init__(self, name, owner):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # On renseigne le nom du propriétaire de notre agenda :
        self.owner = Gtk.Label("Propriétaire :"+ owner, xalign=0)

        # On renseigne le nom de notre agenda :
        self.name = Gtk.Label("Nom : "+ name, xalign=0)

        # On ajoute les éléments à notre boîte :
        self.pack_start(self.owner, True, True, 0)
        self.pack_start(self.name, True, True, 0)