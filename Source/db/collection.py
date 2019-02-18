from core import *
from datetime import datetime

class DbCollection(Collection):
	def __init__(self, cursor):
		super().__init__()

		self.cursor = cursor

		# Liste d'attente pour l'écriture et la modification.
		self.new_queue = []
		self.update_queue = []

	def _get(self, query):
		self._run(query)
		return self.cursor.fetchall()

	def _run(self, query):
		print("[query] {}".format(query))
		self.cursor.execute(query)

	def _get_row(self, _id, table):
		return self._get("SELECT * FROM `{}` WHERE id = {}".format(table, _id))

	def _list_id(self, table, column, _id):
		return self._get("SELECT id FROM `{}` WHERE {} = {}".format(table, column, _id))

	def _last_id(self):
		self._run("SELECT LAST_INSERT_ID()")
		return self.cursor.fetchone()[0]

	def _convert_value(self, value):
		_type = type(value)
		if issubclass(_type, Data) or issubclass(_type, DataProxy):
			return str(value.id)
		if _type is datetime:
			return "\"{}\"".format(value)
		if _type is int:
			return str(value)
		if _type is str:
			return "\"{}\"".format(value)
		if _type is type(None):
			return "-1"

		raise (TypeError("Invalid type {}".format(_type.__name__)))

	def _no_id_attr_names(self, _type):
		if _type is Account:
			return ("login", "mdp", "email")
		if _type is Agenda:
			return ("name", "owner")
		if _type is Event:
			return ("start", "end", "type", "description", "agenda")
		if _type is Group:
			return ("name", )
		if _type is Resource:
			return ("name", "location", "capacity", "group")
		if _type is User:
			return ("first_name", "last_name", "email", "tel", "account")

	def _insert(self, data, _type):
		table = _type.__name__
		# Les attributs à écrire.
		attr = {name : getattr(data, name) for name in self._no_id_attr_names(_type)}
		# Nom des colonnes.
		names = ", ".join("`{}`".format(key) for key in attr.keys())
		# Valeurs des colonnes.
		values = ", ".join((self._convert_value(val)) for val in attr.values())

		# Écriture automatique des champs d'entité
		self._run("INSERT INTO `{}` ({}) VALUES ({})".format(table, names, values))

		data.id = self._last_id()

	def _insert_relation(self, _id, data_list, from_type, to_type, from_attr, to_attr):
		table = "{}_{}".format(from_type.__name__, to_type.__name__)
		for item in data_list:
			self._run("INSERT INTO `{}` (`{}`, `{}`) VALUES ({}, {})".format(table, from_attr, to_attr, _id, item.id))

	def _insert_relations(self, data, _type):
		if _type is Agenda:
			self._insert_relation(data.id, data.linked_agendas, _type, Agenda, "agenda1", "agenda2")
		if _type is Event:
			self._insert_relation(data.id, data.resources, _type, Resource, "event", "resource")
			self._insert_relation(data.id, data.users, _type, User, "event", "user")
		if _type is Group:
			self._insert_relation(data.id, data.admins, _type, User, "group", "admin")
			self._insert_relation(data.id, data.subscribers, _type, User, "group", "user")

	def _delayed_new(self, data, type):
		print("[DB] new {}".format(type.__name__))
		self._insert(data, type)

	def _delayed_new_relation(self, data, type):
		print("[DB] new relation {}".format(type.__name__))
		self._insert_relations(data, type)

	def _new(self, data, type):
		self.new_queue.append((data, type))

	def _load(self, _id, type):
		row = self._get_row(_id, type.__name__)

		if type is Account:
			return Account(_id, self, self._list_id("User", "account", _id), row["login"], row["mdp"], row["email"])
		if type is Agenda:
			return self._load_agenda(_id, row)
		if type is Event:
			return self._load_event(_id, row)
		if type is Group:
			return self._load_group(_id, row)
		if type is User:
			return self._load_user(_id, row)

	def flush(self):
		""" "Commit" les modifications """

		def priority(_type):
			""" Calcul de l'ordre d'ecriture par un numéro de priorité.
			Ceci dans le but d'écrire les données en dépendance après leur
			dépendance. Par exemple écrire en premier les agendas avant leur
			événement pour connaitre l'id de l'agenda à utiliser dans l'événement
			"""
			if _type is Account:
				return 1
			if _type in (User, Group):
				return 2
			if _type in (Agenda, Resource):
				return 3
			if _type is Event:
				return 4

		# Tri par dépendance.
		new_queue = sorted(self.new_queue, key=lambda item: priority(item[1]))
		print([_type.__name__ for data, _type in new_queue])
		for data, type in new_queue:
			self._delayed_new(data, type)

		# Pas de tri pour les relations car toutes les id existent.
		for data, type in self.new_queue:
			self._delayed_new_relation(data, type)