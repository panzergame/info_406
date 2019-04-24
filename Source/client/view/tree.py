# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def diff_list(a, b):
	set_a = set(a)
	set_b = set(b)

	added_keys = set_a - set_b
	removed_keys = set_b - set_a
	kept_keys = set_a & set_b

	return list(added_keys), list(removed_keys), list(kept_keys)

def diff_dict(a, b):
	set_a = set(a.keys())
	set_b = set(b.keys())

	added_keys = set_a - set_b
	removed_keys = set_b - set_a
	kept_keys = set_a & set_b

	added_dict = {key : a[key] for key in added_keys}
	removed_dict = {key : b[key] for key in removed_keys}
	kept_dict = {key : a[key] for key in kept_keys}

	for key in kept_keys:
		if isinstance(a[key], list):
			added, removed, kept = diff_list(a[key], b[key])
			if len(added) > 0:
				added_dict[key] = added
			if len(removed) > 0:
				removed_dict[key] = removed
			if len(kept) > 0:
				kept_dict[key] = kept

	return added_dict, removed_dict, kept_dict

class Tree(Gtk.TreeStore):
	""" Un arbre actualisable qui remplace le minimum de ligne
		pour conserver la vue et notamment les categories étendues.
	"""

	def __init__(self, *format):
		super().__init__(*format)

		self.rows = {}

	def _add(self, iter, d):
		if isinstance(d, list):
			for value in d:
				self.append(iter, value)
		elif isinstance(d, dict):
			for key, values in d.items():
				_iter = self.append(iter, key)
				self._add(_iter, values)

	def _remove(self, iter, d): # TODO
		while iter is not None:
			next_iter = self.iter_next(iter)
			if self[iter][0] in map(lambda x: x[0], d):
				iter = self.remove(iter)
			iter = next_iter

	def set(self, rows):
		# Recherche des différences.
		added_dict, removed_dict, _ = diff_dict(rows, self.rows)
		self.rows = rows

		self._remove(self.get_iter_first(), removed_dict)
		self._add(None, added_dict)
