# -*- coding: utf-8 -*-

from core import *
from datetime import *

class XMLConverter:
	def __init__(self, collection):
		self.collection = collection

	def _attr_to_xml(self, value):
		""" Conversion d'un attribut vers un type supporté par le XML """

		if isinstance(value, DataProxy) or isinstance(value, Data):
			return value.id
		elif isinstance(value, set) or isinstance(value, list) \
			or isinstance(value, WeakRefSet):
			return [self._attr_to_xml(item) for item in value]
		elif isinstance(value, str):
			return value
		elif isinstance(value, datetime):
			return value
		elif isinstance(value, int):
			return value
		else:
			raise TypeError("Unsupported type ", type(value))

	def _attrs_to_xml(self, attrs, data):
		""" Conversion d'un liste d'attribut d'une classe en XML """
		return {attr : self._attr_to_xml(getattr(data, attr)) for attr in attrs}

	def to_xml(self, data):
		if isinstance(data, Account):
			attrs = ("id", "users", "login", "mdp", "email")
		elif isinstance(data, Agenda):
			attrs = ()
		elif isinstance(data, User):
			attrs = ("id", "first_name", "last_name", "email", "tel", "agenda", "groups", "account")
		elif isinstance(data, Event):
			attrs = ()
		elif isinstance(data, Notification):
			attrs = ()
		elif isinstance(data, Agenda):
			attrs = ()
		elif isinstance(data, Group):
			attrs = ()
		else:
			raise TypeError("Invalid data type to XML conversion")

		return self._attrs_to_xml(attrs, data)

	def _id_to_proxy(self, _id, _type):
		return DataProxy(_id, _type, self.collection)

	def _ids_to_proxies(self, ids, _type):
		return {self._id_to_proxy(_id, _type) for _id in ids}

	def to_data(self, _type, xml):
		if _type is Account:
			return Account(xml["id"], self.collection,
				self._ids_to_proxies(xml["users"], User),
				xml["login"], xml["mdp"], xml["email"])
		elif _type is User:
			return User(xml["id"], self.collection,
				xml["first_name"], xml["last_name"],
				xml["email"], xml["tel"],
				self._id_to_proxy(xml["agenda"], Agenda),
				self._ids_to_proxies(xml["groups"], Group),
				self._id_to_proxy(xml["account"], Account))
