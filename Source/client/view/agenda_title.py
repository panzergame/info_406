import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AgendaTitleBox(Gtk.Box):
	def __init__(self, common):
		Gtk.Box.__init__(self)
		self.set_halign(Gtk.Align.CENTER)
		frame=Gtk.Frame()
		self.common = common
		self.title = Gtk.Label()
		self.setTitleString()

		container = Gtk.Box()
		container.set_border_width(5)
		container.add(self.title)
		frame.add(container)

		self.add(frame)
		common.add_observer(self)
	
	def setTitleString(self):
		if self.common.agenda_displayed.user == None:
			self.title.set_text("{} ({})".format(self.common.agenda_displayed.name, self.common.agenda_displayed.group.name))
		else:
			self.title.set_text("Agenda de {} {}".format(self.common.agenda_displayed.user.first_name,self.common.agenda_displayed.user.last_name))
			
	
	def update(self, common):
		self.setTitleString()
