# -*- coding: utf-8 -*-

class Data:
	def __init__(self, _id, collection):
		self.__dict__["id"] = _id
		self.__dict__["collection"] = collection

	@property
	def id(self):
		return self.__dict__["id"]

	def # TODO setter pour eviter appelle __setattr__ pour id (new insert)

	@property
	def collection(self):
		return self.__dict__["collection"]

	def __setattr__(self, name, value):
		""" Detection du changement d'une valeur """
		self.update()
		print(name)
		self.__dict__[name] = value

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
		print("update")
		self.collection.update(self)
