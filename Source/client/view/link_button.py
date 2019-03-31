import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Link_Button(Gtk.Button):
	def __init__(self, agenda, common):
		Gtk.Button.__init__(self)
		self.agenda = agenda
		self.common = common
		self.set_title()


	def is_linked(self, agenda):
		user_linked_agendas = self.common.user_clicked._agenda.linked_agendas
		if (agenda in user_linked_agendas):
			res = True
		else:
			res = False
		return res

	def set_title(self):
		if (self.is_linked(self.agenda)):
			title = Gtk.Label("Délier", xalign=0)
		else:
			title = Gtk.Label("Lier", xalign=0)
		self.add(title)
