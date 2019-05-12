from client.view.group_permission_manager import *
from client.model.collection import *

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

##########################
# Permet de modifier les permissions d'un group arbitraire de la BDD
##########################
collec = ClientCollection()
for one_group in collec.load_groups(""):
	group = one_group
	break

d = PermManagementDialog(group)
d.run()
Gtk.main()
