class DataProxy:
	def __init__(self, _id, type, collection):
		self.id = _id
		self.type = type
		self.collection = collection
		self.data = None

	def __getattr__(self, name):
		if self.data is None:
			self.data = self.collection.load(self.id, self.type)

		return getattr(self.data, name)

	def __repr__(self):
		return "[Proxy of {} : {}]".format(self.type.__name__, "not loaded" if self.data is None else self.data)
