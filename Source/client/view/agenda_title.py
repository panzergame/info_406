import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .observer import *

class AgendaTitleBox(Gtk.HeaderBar, ViewObserver):
	def __init__(self, common):
		Gtk.HeaderBar.__init__(self)
		ViewObserver.__init__(self, common, common.agenda_displayed)

		self.setTitleString()

	def setTitleString(self):
		ag = self.common.agenda_displayed.value
		if ag is not None:
			user = ag.user
			if user is None:
				text = "{} ({})".format(ag.name, ag.group.name)
			else:
				text = "Agenda de {} {}".format(user.first_name, user.last_name)

			self.props.title = text
	
	def update(self):
		self.setTitleString()
