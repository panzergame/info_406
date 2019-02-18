import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#######################################################################################################################

# Classe définissant une liste de groupes :

class GroupList(Gtk.Box):
    # On appelle le constructeur de la classe mère avec un agencement vertical et un espacement entre éléments
    # de 6 pixels :
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing = 6)
        # Actions sur les attributs :

        # On donne un titre à notre boîte :
        self.title = Gtk.Label("\tGroupes : ", xalign=0)

        # On donne une liste en attribut :
        self.groupList = Gtk.ListBox()

        # On ajoute ce titre à notre boîte :
        self.pack_start(self.title, False, True, 0)

        # On ajoute cette liste à notre boîte :
        self.pack_start(self.groupList, True, True, 0)

    # Méthodes :

    # On definie la méthode permettant d'ajouter un groupe à notre boîte :
    def addGroup(self, name):
        group = Group(name)
        self.groupList.add(group)


#######################################################################################################################

# Classe definissant un groupe :

class Group(Gtk.ListBoxRow):
    # On appelle le constructeur de la classe mère :
    def __init__(self, name):
        Gtk.ListBoxRow.__init__(self)

        # Actions sur les attributs :

        # On donne une boite horizontale en attribut :
        self.groupLine = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing = 6)

        # On crée un bouton de couleur (qui sera associée au groupe) :
        self.color = Gtk.ColorButton()

        # On crée un label avec le nom de notre groupe :
        self.name = Gtk.Label(name, xalign=0)

        # On crée la liste d'agendas liée à notre ligne (groupe) :
        self.agendasList = Gtk.ListBox()

        # On ajoute la couleur, le nom et la liste d'agendas à notre groupe (groupLine) :
        self.groupLine.pack_start(self.color, False, True, 0)
        self.groupLine.pack_start(self.name, False, True, 0)
        self.groupLine.pack_start(self.agendasList, False, True, 0)

        # On ajoute notre boite groupLine à notre ligne (Group) qui contiendra les agendas de son groupe associé :
        self.add(self.groupLine)

    # Méthodes :

    # On definie la méthode nous permettant d'ajouter un agenda :
    def addAgenda(self, name, owner):
        agenda = Agenda(name, owner)
        self.agendasList.add(agenda)


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


#######################################################################################################################

# Classe definissant un Evènement :

"""class Event(Gtk.Box)
    # On appelle le constructeur de la classe mère avec un agencement vertical et un espacement entre éléments
    # de 6 pixels :
    def __init__(self, desc):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        # On renseigne la description de l'évènement :
        self.desc = Gtk.Label("Propriétaire :"+ desc, xalign=0)

        # On ajoute ce label à notre boite :
        self.pack_start(self.desc, True, True, 0)
"""