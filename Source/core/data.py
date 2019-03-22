# -*- coding: utf-8 -*-

class Data:
	def __init__(self, _id, collection):
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

	def delete(self):
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
		return hash(type(self)) ^ hash(self.id)

	def __eq__(self, other):
		return hash(self) == hash(other)
