# -*- coding: utf-8 -*-

from core import *
from .converter import *

class Server:
	def __init__(self, collection):
		self.collection = collection
		self.converter = XMLConverter(self.collection)
		self.session_id = 0
		self.sessions = {}

	def load(self, _id, type_name):
		type = supported_types_name[type_name]
		data = self.collection.load(_id, type)

		return self.converter.to_xml(data)

	def new(self, data, type_name):
		type = supported_types_name[type_name]
		data = self.collection.new(data, type)

		return self.converter.to_xml(data)

	def connect(self, user, password):
		if not user in self.sessions:
			_id = self.sessions[user] = self.session_id
			self.session_id += 1
			return _id

		return self.sessions[user]
