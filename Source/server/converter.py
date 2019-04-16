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
		elif value is None:
			return value
		else:
			raise TypeError("Unsupported type {}".format(type(value)))

	def _attrs_to_xml(self, attrs, data):
		""" Conversion d'un liste d'attribut d'une classe en XML """
		return {attr : self._attr_to_xml(getattr(data, attr)) for attr in attrs}

	def to_xml(self, data):
		if isinstance(data, set) or isinstance(data, list):
			return [self.to_xml(item) for item in data]
		elif isinstance(data, DataProxy):
			return data.id
		else:
			if isinstance(data, Account):
				attrs = ("users", "login", "mdp", "email")
			elif isinstance(data, Agenda):
				attrs = ("name", "linked_agendas", "notifications", "ignored_events", "last_sync", "user", "group")
			elif isinstance(data, User):
				attrs = ("first_name", "last_name", "email", "tel", "agenda", "groups", "account")
			elif isinstance(data, Event):
				attrs = ("start", "end", "type", "description", "agenda", "creation_date", "users", "resources")
			elif isinstance(data, Notification):
				attrs = ("event", "agenda", "status")
			elif isinstance(data, Agenda):
				attrs = ("name", "last_sync", "user", "group", "linked_agendas", "notifications", "ignored_events")
			elif isinstance(data, Group):
				attrs = ("name", "admins", "subscribers", "agendas", "resources")
			elif isinstance(data, Resource):
				attrs = ("name", "location", "capacity", "group")
			else:
				raise TypeError("Invalid data type to XML conversion {}".format(type(data)))

			# Attributs communs.
			common_attrs = ("id", )

			return self._attrs_to_xml(attrs + common_attrs, data)

	def queue_to_xml(self, queue):
		xml = {}

		for data in queue:
			# Convertion d'un élément en XML.
			data_xml = self.to_xml(data)

			# Association dans une categorie par type.
			type_name = type(data).__name__
			if type_name in xml:
				xml[type_name].append(data_xml)
			else:
				xml[type_name] = [data_xml]

		return xml

	def xml_to_queue(self, xml):
		queue = set()
		for type_name, xml_datas in xml.items():
			_type = self.collection.supported_types_name[type_name]
			queue |= self.to_datas(_type, xml_datas)

		return queue

	def _id_to_proxy(self, _id, _type):
		return self.collection._data_or_proxy(_id, _type)

	def _ids_to_proxies(self, ids, _type):
		return {self._id_to_proxy(_id, _type) for _id in ids}

	def to_datas(self, _type, xml):
		return {self.to_data(_type, subxml) for subxml in xml}

	def to_data(self, _type, xml):
		# Support des proxies.
		if isinstance(xml, int):
			return self.collection._data_or_proxy(xml)

		_id = xml["id"]
		if issubclass(_type, Account):
			return _type(_id, self.collection,
				xml["login"], xml["mdp"], xml["email"],
				self._ids_to_proxies(xml["users"], User))
		if issubclass(_type, User):
			return _type(_id, self.collection,
				xml["first_name"], xml["last_name"],
				xml["email"], xml["tel"],
				self._id_to_proxy(xml["agenda"], Agenda),
				self._ids_to_proxies(xml["groups"], Group),
				self._id_to_proxy(xml["account"], Account))
		if issubclass(_type, Group):
			return _type(_id, self.collection,
				xml["name"],
				self._ids_to_proxies(xml["admins"], User),
				self._ids_to_proxies(xml["subscribers"], User),
				self._ids_to_proxies(xml["agendas"], Agenda),
				self._ids_to_proxies(xml["resources"], Resource))
		if issubclass(_type, Agenda):
			return _type(_id, self.collection,
				xml["name"],
				self._ids_to_proxies(xml["linked_agendas"], Agenda),
				self._ids_to_proxies(xml["notifications"], Notification),
				self._ids_to_proxies(xml["ignored_events"], Event))
		if issubclass(_type, Event):
			return _type(_id, self.collection,
				xml["start"], xml["end"], xml["type"],
				xml["description"],
				self._ids_to_proxies(xml["resources"], Resource),
				self._ids_to_proxies(xml["users"], User),
				self._id_to_proxy(xml["agenda"], Agenda))
		if issubclass(_type, Notification):
			return _type(_id, self.collection,
				self._id_to_proxy(xml["event"], Event),
				self._id_to_proxy(xml["agenda"], Agenda),
				xml["status"])
		if issubclass(_type, Resource):
			return _type(_id, self.collection,
				xml["name"], xml["location"], xml["capacity"],
				self._id_to_proxy(xml["group"], Group))

