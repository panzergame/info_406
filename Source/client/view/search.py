import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SearchBox(Gtk.Box):

    def __init__(self):
        Gtk.Box.__init__(self,orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_border_width(10)

        title = Gtk.Label("Rechercher un groupe")

        entry = Gtk.Entry()
        entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "system-search-symbolic")

        buttonSearch = Gtk.Button(label="Rechercher")
        buttonSearch.connect("clicked", self.on_button_search_clicked)

        searchZone = Gtk.Box(spacing=6)

        searchZone.pack_start(entry, True, True, 0)
        searchZone.pack_start(buttonSearch, False, False, 0)

        self.pack_start(title, True, True, 0)
        self.pack_start(searchZone, True, True, 0)

    def on_button_search_clicked(self, widget):
        gpe = self.entry.get_text()
