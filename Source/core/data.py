# -*- coding: utf-8 -*-

from .dataweak import *

class Data(WeakRefered):
	def __init__(self, _id, collection):
		super().__init__()

		self.id = _id
		self.collection = collection

	# Interface CRUD

	@classmethod
	def new(cls, collection, *args):
		# Enregistrement de la donnée dans la collection et création d'un id.
		return collection.new(cls, *args)

	@classmethod
	def load(cls, collection, _id):
		return collection.load(_id, cls)

	def delete(self, owner=None):
		super().delete()

		self.collection.delete(self)

	def update(self):
		self.collection.update(self)

	def update_relations(self):
		""" Actualisation des relations seulements.
		Par exemple lors d'ajout d'un utilisateur dans un groupe,
		d'un administrateur.
		"""
		self.collection.update_relations(self)

	def __hash__(self):
		if self.id != -1:
			return hash(type(self)) ^ hash(self.id)
		# Pour une donnée pas encore enregistré (sans id), utilisation du hash de base.
		return super().__hash__()

	def __eq__(self, other):
		return hash(self) == hash(other)
