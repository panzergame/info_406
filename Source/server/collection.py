# -*- coding: utf-8 -*-

from .converter import *

class ClientCollection(Collection):
	def __init__(self, server):
		super().__init__()

		self.converter = XMLConverter(self)
		self.server = server

	def load(self, proxy):
		xml = self.server.load(_id, _type.__name__)
		print(xml, _type)
		return self.converter.to_data(_type, xml)

	def load_events(self, agenda, from_date, to_date):
		pass

	def new(self, _type, *args):
		pass

	def delete(self, data):
		pass

	def delete_proxy(self, proxy):
		pass

	def update(self, data):
		pass

	def update_relations(self, data):
		pass

	def flush(self):
		pass
