import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AgendaTitleBox(Gtk.HeaderBar):
	def __init__(self, common):
		Gtk.HeaderBar.__init__(self)
		self.common = common
		self.common.add_observer(self)

		#self.set_property("hexpand", True)

		self.setTitleString()

	def setTitleString(self):
		if self.common.agenda_displayed is not None:
			if self.common.agenda_displayed.user is None:
				text = "{} ({})".format(self.common.agenda_displayed.name, self.common.agenda_displayed.group.name)
			else:
				text = "Agenda de {} {}".format(self.common.agenda_displayed.user.first_name,self.common.agenda_displayed.user.last_name)

			self.props.title = text
	
	def update(self, common):
		self.setTitleString()
