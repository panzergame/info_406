# -*- coding: utf-8 -*-

from core import *
from datetime import datetime

class DbCollection(Collection):
	def __init__(self, cursor):
		super().__init__()

		# Toutes les données existant aussi dans le base et chargé.
		self._datas = {type : {} for type in supported_types}

		self.cursor = cursor

		# Liste d'attente pour l'écriture et la modification.
		self.new_queue = []
		self.update_queue = []
		self.delete_queue = []

	def _get(self, query):
		""" Execution d'un requéte et récupération du résultat sous la forme d'un tableau de dictionnaire """
		self._run(query)
		rows = self.cursor.fetchall()
		fields = list(map(lambda x: x[0], self.cursor.description))
		return [{fields[i] : self._convert_sql_to_value(row[i]) for i in range(0, len(fields))}
					for row in rows]

	def _run(self, query):
		print("[query] {}".format(query))
		self.cursor.execute(query)

	def _get_row(self, _id, table):
		return self._get("SELECT * FROM `{}` WHERE id = {}".format(table, _id))

	def _list_id(self, _type, attr, _id):
		table = _type.__name__
		return self._list_relation(table, _type, attr, _id, "id")

	def _list_relation(self, table, _type, from_attr, from_value, to_attr):
		rows = self._get("SELECT `{}` FROM `{}` WHERE `{}` = {}".format(to_attr, table, from_attr, from_value))
		return set(map(lambda x: self._convert_sql_id(x[to_attr], _type), rows))

	def _last_id(self):
		self._run("SELECT LAST_INSERT_ID()")
		return self.cursor.fetchone()[0]

	def _convert_sql_id(self, id, _type):
		return DataProxy(id, _type, self)

	def _convert_sql_to_value(self, sql):
		if sql == -1:
			return None
		return sql

	def _convert_value_to_sql(self, value):
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
			return ("name", "group", "user")
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
		values = ", ".join(self._convert_value_to_sql(val) for val in attr.values())

		# Écriture automatique des champs d'entité
		self._run("INSERT INTO `{}` ({}) VALUES ({})".format(table, names, values))

		data.id = self._last_id()

	def _insert_relation(self, _id, data_list, table, from_attr, to_attr):
		for item in data_list:
			self._run("INSERT INTO `{}` (`{}`, `{}`) VALUES ({}, {})".format(table, from_attr, to_attr, _id, item.id))

	def _insert_relations(self, data, _type):
		if _type is Agenda:
			self._insert_relation(data.id, data.linked_agendas, "Agenda_Agenda", "agenda1", "agenda2")
		if _type is Event:
			self._insert_relation(data.id, data.resources, "Event_Resource", "event", "resource")
			self._insert_relation(data.id, data.users, "Event_User", "event", "user")
		if _type is Group:
			self._insert_relation(data.id, data.admins, "Group_Admin", "group", "admin")
			self._insert_relation(data.id, data.subscribers, "Group_User", "group", "user")

	def _delayed_new(self, data, type):
		print("[DB] new {}".format(type.__name__))
		self._insert(data, type)

		# Enregistrement de la donnée par id après sa création
		category = self._datas[type]
		category[data.id] = data

	def _delayed_new_relation(self, data, type):
		print("[DB] new relation {}".format(type.__name__))
		self._insert_relations(data, type)

	def new(self, data, type):
		self.new_queue.append((data, type))

		return data

	def load(self, _id, type):
		# Recherche dans le cache
		category = self._datas[type]
		if _id not in category:
			category[_id] = self._load(_id, type)
		return category[_id]


	def _load(self, _id, type):
		row = self._get_row(_id, type.__name__)[0]

		if type is Account:
			return Account(_id, self,
					self._list_id(User, "account", _id), row["login"], row["mdp"], row["email"])
		if type is Agenda:
			return Agenda(_id, self, row["name"],
					self._list_id(Event, "agenda", _id),
					self._list_relation("Agenda_Agenda", Agenda, "agenda1", _id, "agenda2"),
					self._convert_sql_id(row["user"], User), self._convert_sql_id(row["group"], Group))
		if type is Event:
			return Event(_id, self, row["start"], row["end"], row["type"], row["description"],
					self._list_relation("Event_Resource", Resource, "event", _id, "resource"),
					self._list_relation("Event_User", User, "event", _id, "user"),
					self._convert_sql_id(row["agenda"], Agenda))
		if type is Group:
			return Group(_id, self, row["name"],
					self._list_relation("Group_Admin", User, "group", _id, "admin"),
					self._list_relation("Group_User", User, "group", _id, "user"),
					self._list_id(Agenda, "group", _id),
					self._list_id(Resource, "group", _id))
		if type is User:
			return User(_id, self, row["first_name"], row["last_name"], row["email"], row["tel"],
			   list(self._list_id(Agenda, "user", _id))[0],
			   self._list_relation("Group_User", Group, "user", _id, "group"),
			   self._convert_sql_id(row["account"], Account))

	def _delayed_update(self, data, _type):
		table = _type.__name__
		# Les attributs à écrire.
		attr = {name : getattr(data, name) for name in self._no_id_attr_names(_type)}
		# Liste de pair nom = valeur
		assignements = ", ".join("`{}` = {}".format(name, self._convert_value_to_sql(value)) for name, value in attr.items())
		# Écriture automatique des champs d'entité
		self._run("UPDATE `{}` SET {} WHERE `id` = {}".format(table, assignements, data.id))

	def _delayed_update_relation(self, data, _type):
		self._delete_relations(data, _type)
		self._insert_relations(data, _type)

	def update(self, data, type):
		self.update_queue.append((data, type))

	def _delayed_delete(self, data, type):
		table = type.__name__
		self._run("DELETE FROM `{}` WHERE `id` = {}".format(table, data.id))

	def _delayed_delete_relation(self, data, _type):
		self._delete_relations(data, _type)

	def _delete_relation(self, _id, table, attr):
		self._run("DELETE FROM `{}` WHERE `{}` = {}".format(table, attr, _id))

	def _delete_relations(self, data, _type):
		if _type is Agenda:
			self._delete_relation(data.id, "Agenda_Agenda", "agenda1")
			self._delete_relation(data.id, "Agenda_Agenda", "agenda2")
		if _type is Event:
			self._delete_relation(data.id, "Event_Resource", "event")
			self._delete_relation(data.id, "Event_User", "event")
		if _type is Group:
			self._delete_relation(data.id, "Group_Admin", "group")
			self._delete_relation(data.id, "Group_User", "group")

	def delete(self, data, type):
		self.delete_queue.append((data, type))

		self._datas[type].pop(data.id)

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
		for data, type in new_queue:
			self._delayed_new(data, type)

		# Pas de tri pour les relations car toutes les id existent.
		for data, type in self.new_queue:
			self._delayed_new_relation(data, type)

		for data, type in self.update_queue:
			self._delayed_update(data, type)
			self._delayed_update_relation(data, type)

		for data, type in self.delete_queue:
			self._delayed_delete(data, type)
			self._delayed_delete_relation(data, type)

		self.new_queue.clear()
		self.update_queue.clear()
		self.delete_queue.clear()
