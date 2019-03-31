import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class GroupBox(Gtk.Box):
	def __init__(self, common):
		Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.title = Gtk.Label("\tGroupes : ", xalign=0)
		self.add(self.title)
		self._create(common)
		common.add_observer(self)

	def _create(self, common):
		self.groupList = self.put_groups(common)
		self.add(self.groupList)

	def update(self, common):
		self.remove(self.groupList)
		self._create(common)
		self.show_all()

	def put_groups(self, common):
		user = common.user_clicked
		groupList = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		groups = user.groups
		for group in groups:
			groupLine = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
			color = Gtk.ColorButton()
			name = Gtk.Label(group.name, xalign=0)
			agendasList = self.put_agendas(group, common)
			groupLine.pack_start(color, False, True, 0)
			groupLine.pack_start(name, False, True, 0)
			groupLine.pack_start(agendasList, False, True, 0)
			groupList.add(groupLine)
		return groupList

	def put_agendas(self, group, common):
		agendasList = Gtk.ListBox()
		agendas = group.agendas
		for agenda in agendas:
			name = Gtk.Label(agenda.name, xalign=0)
			agendasList.add(name)
		return agendasList
