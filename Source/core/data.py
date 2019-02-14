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
		self.collection.update(self, type(self))

	def _all_attrs(self, predica):
		""" Renvoie tous les attributs filtré par un prédicat de type """
		all_attrs = set(dir(self)) - set(dir(type(self)))
		return {name : getattr(self, name) \
				for name in all_attrs \
					if predica(type(getattr(self, name)))}

	@property
	def relations(self):
		""" Renvoie les attributs des relations N:M """
		self._all_attrs(lambda type : (type in (set, list)))

	@property
	def attributes(self):
		""" Renvoie les attributs d'entité et les relations 1:N """
		self._all_attrs(lambda type : (type not in (set, list)))
