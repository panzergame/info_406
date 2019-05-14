from client.view.group_permission_manager import *
from client.model.collection import *

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

##########################
# Permet de modifier les permissions d'un group arbitraire de la BDD
##########################
collec = ClientCollection()

#Manière dégueulasse de sélectionner un groupe dans le set retourné par la méthode load, donc un groupe alétoire de la bdd
list_of_groups=[]
for one_group in collec.load_groups(""):
	list_of_groups.append(one_group)

d = PermManagementDialog(list_of_groups[0])
d.run()
Gtk.main()
