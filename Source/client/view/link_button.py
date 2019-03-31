import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class LinkButton(Gtk.Button):
	def __init__(self, common, target_agenda):
		Gtk.Button.__init__(self)
		self.target_agenda = target_agenda
		self.common = common
		self.set_title()
		self.connect("clicked", self.set_link)


	def is_linked(self):
		user_linked_agendas = self.common.user_clicked._agenda.linked_agendas
		return target_agenda in user_linked_agendas

	def set_title(self):
		if (self.is_linked()):
			title = "Délier"
		else:
			title = "Lier"
		self.set_label(title)

	def set_link(self, button, common):
		current_user_agenda = common.user_clicked.agenda
		if (self.is_linked()):
			current_user_agenda.unlink_agenda(target_agenda)
		else:
			current_user_agenda.link_agenda(target_agenda)

		self.update()
	
	def update(self):
		self.set_title()

