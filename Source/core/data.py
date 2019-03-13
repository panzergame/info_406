# -*- coding: utf-8 -*-

class Data:
	def __init__(self, _id, collection):
		self.id = _id
		self.collection = collection

	# Interface CRUD

	@classmethod
	def new(cls, collection, *args):
		# Création de la donnée.
		data = cls(-1, collection, *args)
		# Enregistrement de la donnée dans la collection et création d'un id.
		return collection.new(data, cls)

	@classmethod
	def load(cls, collection, _id):
		return collection.load(_id, cls)

	def delete(self):
		self.collection.delete(self, type(self))

	def update(self):
		print(id(self), self, type(self))
		self.collection.update(self, type(self))
