import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from dateTime import *

class AddEventDialog(Gtk.Dialog):
	def __init__(self, parent, agenda):
		Gtk.Dialog.__init__(self, "Ajouter un événement", parent, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OK, Gtk.ResponseType.OK))

		type = Gtk.Entry()
		type.set_text("type")

		description = Gtk.Entry()
		description.set_text("description")

		start = Gtk.Button("début")
		start.connect("clicked", self.on_start_clicked)

		end = Gtk.Button("fin")
		end.connect("clicked", self.on_end_clicked)

		box = self.get_content_area()
		box.add(type)
		box.add(description)

		row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		row.pack_start(start, True, True, 0)
		row.pack_start(Gtk.Label("jusqu'à"), True, True, 0)
		row.pack_start(end, True, True, 0)

		box.pack_start(row, True, True, 0)

	def on_start_clicked(self, button):
		date = DateTimeBox(self)

		if date.run() == Gtk.ResponseType.OK:
			pass

		date.destroy()

	def on_end_clicked(self, button):
		date = DateTimeBox(self)

		if date.run() == Gtk.ResponseType.OK:
			pass

		date.destroy()

window = Gtk.Window()
window.show_all()

dia = AddEventDialog(window, None)
dia.show_all()

dia.run()
dia.destroy()

Gtk.main()
