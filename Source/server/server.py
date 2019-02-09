from core import *

class Server:
	def __init__(self, collection):
		self.collection = collection
		self.session_id = 0
		self.sessions = {}

	def _dump_proxy(self, proxy):
		return {"id" : proxy.id, "type" : proxy.type.__name__}

	def _dump(self, data):
		data_type = type(data)

		attrs = {name : getattr(data, name) for name in dir(data) if name not in dir(data_type)}

		for name, value in attrs.items():
			if type(value) == DataProxy:
				attrs[name] = self._dump_proxy(value)

		return attrs

	def load(self, _id, type_name):
		type = supported_types_name[type_name]
		data = self.collection.load(_id, type)

		return self._dump(data)

	def connect(self, user, password):
		if not user in self.sessions:
			_id = self.sessions[user] = self.session_id
			self.session_id += 1
			return _id

		return self.sessions[user]
