import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class LinkButton(Gtk.Button):
	def __init__(self, common):
		Gtk.Button.__init__(self)
		self.common=common
		self.set_title()
		self.connect("clicked", self.set_link, common)


	def is_linked(self, agenda):
		user_linked_agendas = self.common.user_clicked._agenda.linked_agendas
		if (agenda in user_linked_agendas):
			res = True
		else:
			res = False
		return res

	def set_title(self):
		if (self.is_linked(self.common.agenda_displayed)):
			title = "Délier"
		else:
			title = "Lier"
		self.set_label(title)

	def set_link(self, button, common):
		current_user_agenda = common.user_clicked.agenda
		if (self.is_linked(self.common.agenda_displayed)):
			current_user_agenda.unlink_agenda(common.agenda_displayed)
		else:
			current_user_agenda.link_agenda(common.agenda_displayed)

		self.update()
	
	def update(self):
		self.set_title()

