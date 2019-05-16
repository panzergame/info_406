# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class SuppConfirmDialog(Gtk.Dialog):
	def __init__(self):
		Gtk.Dialog.__init__(self, "Suppression d'utilisateur(s):", None, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OK, Gtk.ResponseType.OK))

		msg = Gtk.Label("Êtes-vous sûr de vouloir supprimer le(s) utilisateur(s) sélectionné(s) ?\n"
						"Cette opération est irréversible.")

		box = self.get_content_area()
		box.add(msg)
		self.show_all()
