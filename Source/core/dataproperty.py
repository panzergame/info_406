# -*- coding: utf-8 -*-

class DataProperty(property):
	def __init__(self, attr_name):
		# Nom privée de l'attribut
		hide_attr_name = "_" + attr_name
		def getter(inst):
			return getattr(inst, hide_attr_name)

		def setter(inst, value):
			inst.update()
			return setattr(inst, hide_attr_name, value)

		super().__init__(getter, setter)

class DataOwnerProperty(property):
	def __init__(self, attr_name):
		# Nom privée de l'attribut
		hide_attr_name = "_" + attr_name
		def getter(inst):
			return getattr(inst, hide_attr_name)

		def setter(inst, value):
			# Changement de referrence.

			prev_reffered = getter(inst)
			# Suppression de l'ancienne.
			if prev_reffered is not None:
				prev_reffered.del_ref(inst)

			# Ajout d'une nouvelle.
			if value is not None:
				value.new_ref(inst)

			inst.update()

			return setattr(inst, hide_attr_name, value)

		super().__init__(getter, setter)

	@staticmethod
	def init(reffered, refferer):
		""" Initialise une référence faible
		Utilisé dans le constructeur sans passer par le setter
		de DataOwnerProperty qui va appeller update()
		"""
		if reffered is not None:
			reffered.new_ref(refferer)

		return reffered
