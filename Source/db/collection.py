# -*- coding: utf-8 -*-

"""
DELIMITER $$

CREATE TRIGGER `delete_User` AFTER DELETE ON `User` FOR EACH ROW
BEGIN
  INSERT INTO `Delete` VALUES (OLD.id, "User");
END $$

DELIMITER ;
"""

from core import *
from datetime import datetime

from .user import *
from .group import *
from .agenda import *
from .event import *
from .resource import *
from .account import *
from .notification import *

# Tous les types supportés.

supported_types = {
	Account : DbAccount,
	Agenda : DbAgenda,
	Event : DbEvent,
	Group : DbGroup,
	User : DbUser,
	Resource : DbResource,
	Notification : DbNotification
}

class DbCollection(Collection):
	def __init__(self, cursor):
		super().__init__()

		# Toutes les données existant dynamiquement ou dans le base et chargé.
		self._datas = {type : {} for type in supported_types.values()}
		# Tous les proxies de données fournis.
		self._data_proxies = {type : {} for type in supported_types.values()}

		self.cursor = cursor

		# Liste d'attente pour l'écriture et la modification.
		self.new_queue = set()
		self.update_queue = set()
		self.update_relations_queue = set()
		self.delete_queue = set()

############### OUTILS ###############

	def _register_data(self, data):
		_type = self._translate_type(data.data_type)

		assert(data.id != -1)

		self._datas[_type][data.id] = data

	def _unregister_data(self, data):
		print(data)
		_type = self._translate_type(data.data_type)

		assert(data.id != -1)

		self._datas[_type].pop(data.id)

	def _register_proxy(self, proxy):
		_type = self._translate_type(proxy.data_type)

		self._data_proxies[_type][proxy.id] = proxy

	def _unregister_proxy(self, proxy):
		_type = self._translate_type(proxy.data_type)

		self._data_proxies[_type].pop(proxy.id)

	def _translate_type(self, _type):
		""" Traduit un type vers un type préfixé par Db
		autremenet dit un type specialisé pour la BDD.
		"""
		if _type in supported_types.keys():
			return supported_types[_type]
		elif _type in supported_types.values():
			return _type

		return None

	def _get(self, query):
		""" Execution d'un requête et récupération du résultat sous la forme d'un tableau de dictionnaire """
		self._run(query)
		rows = self.cursor.fetchall()
		fields = list(map(lambda x: x[0], self.cursor.description))
		return [{fields[i] : row[i] for i in range(0, len(fields))}
					for row in rows]

	def _run(self, query):
		""" Execution d'une requête """
		print("[query] {}".format(query))
		self.cursor.execute(query)

	def _get_row_attr(self, attr, value, table, close=""):
		""" Obtention d'une ligne par un attribut """
		return self._get("SELECT * FROM `{}` WHERE `{}` = {} {}".format(table, attr, value, close))

	def _get_row(self, _id, table):
		""" Obtention d'une ligne par son id """
		return self._get_row_attr("id", _id, table)

	def _list_id(self, _type, attr, value):
		""" Obtention de l'id ou attr = value """
		table = _type.db_table
		return self._list_relation(table, _type, attr, value, "id")

	def _list_id_close(self, _type, close):
		""" Obtention de l'id ou close est vrai """
		table = _type.db_table
		return self._list_relation_close(table, _type, close, "id") # TODO enregister proxy

	def _list_relation(self, table, _type, from_attr, from_value, to_attr):
		""" Obtention d'une colonne (to_attr) de plusieurs lignes avec la contrainte
			from_attr = from_value
		"""
		close = "`{}` = {}".format(from_attr, from_value)
		return self._list_relation_close(table, _type, close, to_attr)

	def _list_relation_close(self, table, _type, close, to_attr):
		""" Obtention d'une colonne (to_attr) de plusieurs lignes avec la close """
		rows = self._get("SELECT `{}` FROM `{}` WHERE {}".format(to_attr, table, close))

		if len(rows) == 0:
			return set()
		return set(map(lambda x: self._convert_sql_id(x[to_attr], _type), rows))

	def _last_id(self):
		""" Récupère l'id de la dernière ligne insérée """
		self._run("SELECT LAST_INSERT_ID()")
		return self.cursor.fetchone()[0]

	def _convert_sql_id(self, id, _type):
		if id is None:
			return None

		""" Conversion d'un numéro issue d'une requête en proxy """
		if type(id) not in (int, type(None)):
			raise TypeError("SQL id should be int")

		# Recherche d'une donnée déjà existante.
		data = self._datas[_type].get(id, None)
		if data is not None:
			return data

		# Recherche d'un proxy déjà existant.
		proxy = self._data_proxies[_type].get(id, None)
		if proxy is not None:
			return proxy

		# Création d'un nouveau proxy.
		proxy = DataProxy(id, _type, self)
		self._data_proxies[_type][id] = proxy

		return proxy

	def _convert_value_to_sql(self, value):
		""" Conversion d'une valeur python en format sql """
		_type = type(value)
		if issubclass(_type, Data) or issubclass(_type, DataProxy):
			return str(value.id)
		if _type is datetime:
			return "\"{}\"".format(value)
		if _type is int:
			return str(value)
		if _type is str:
			return "\"{}\"".format(value)
		if value is None:
			return "NULL"

		raise (TypeError("Invalid type {}".format(_type.__name__)))

############### CRUD MYSQL ###############

	def _insert(self, table, data, fields):
		# Les attributs à écrire.
		attr = {name : getattr(data, name) for name in fields}
		# Nom des colonnes.
		names = ", ".join("`{}`".format(key) for key in attr.keys())
		# Valeurs des colonnes.
		values = ", ".join(self._convert_value_to_sql(val) for val in attr.values())

		# Écriture automatique des champs d'entité
		self._run("INSERT INTO `{}` ({}) VALUES ({})".format(table, names, values))

		data.id = self._last_id()

	def _delete(self, table, _id):
		self._run("DELETE FROM `{}` WHERE `id` = {}".format(table, _id))

	def _euthanasy_proxies(self, _type, attr, _id):
		""" Détection des proxies qui devrait être supprimé
		après la suppression d'une donnée parent.
		Par exemple la suppression d'un Account doit supprimer
		les proxies User obtenus par les groupes.
		"""

		_type = self._translate_type(_type)

		# Les proxies à supprimer.
		proxies = set()

		rows = self._get("SELECT `id` FROM `{}` WHERE `{}` = {}".format(_type.db_table, attr, _id))

		category = self._data_proxies[_type]
		for sub_id in map(lambda row : row["id"], rows):
			# Recherche d'un proxy existant correspondant à une donnée à supprimer.
			proxy = category.get(sub_id, None)

			if proxy is not None:
				proxies.add(proxy)

			# Recherche en cascade d'autres proxies de plus bas niveau.
			else:
				proxies |= _type.db_delete_proxies(self, sub_id)

		return proxies

	def _delete_proxies(self, proxies):
		for proxy in proxies:
			proxy.delete()

	def _update(self, table, data, fields):
		# Les attributs à écrire.
		attr = {name : getattr(data, name) for name in fields}
		# Liste de pair nom = valeur
		assignements = ", ".join("`{}` = {}".format(name, self._convert_value_to_sql(value)) for name, value in attr.items())
		# Écriture automatique des champs d'entité
		self._run("UPDATE `{}` SET {} WHERE `id` = {}".format(table, assignements, data.id))

	def _insert_relation(self, _id, data_list, table, from_attr, to_attr):
		for item in data_list:
			self._run("INSERT INTO `{}` (`{}`, `{}`) VALUES ({}, {})".format(table, from_attr, to_attr, _id, item.id))

	def _delete_relation(self, _id, table, attr):
		self._run("DELETE FROM `{}` WHERE `{}` = {}".format(table, attr, _id))

##############################################

	def _delayed_new(self, data):
		data.db_new()

		# Enregistrement de la donnée par id après sa création
		self._register_data(data) # TODO enregistrer même avec -1 ?

	def _delayed_update(self, data):
		data.db_update()

	def _delayed_delete(self, _type, _id):
		_type.db_delete(self, _id)

	def _delayed_new_relation(self, data):
		data.db_insert_relations()

	def _delayed_update_relation(self, data):
		data.db_delete_relations(self, data.id)
		data.db_insert_relations()

	def _delayed_delete_relation(self, _type, _id):
		_type.db_delete_relations(self, _id)

	def _load(self, _id, type, row):
		if type is DbAccount:
			return DbAccount(_id, self,
					row["login"], row["mdp"], row["email"],
					self._list_id(DbUser, "account", _id))
		if type is DbAgenda:
			return DbAgenda(_id, self, row["name"],
					self._list_relation("Agenda_Agenda", DbAgenda, "agenda1", _id, "agenda2"),
					self._list_id(DbNotification, "agenda", _id),
					self._list_relation("Agenda_Ignore_Event", DbEvent, "agenda", _id, "event"),
					row["last_sync"],
					self._convert_sql_id(row["user"], DbUser), self._convert_sql_id(row["group"], DbGroup))
		if type is DbEvent:
			return DbEvent(_id, self, row["start"], row["end"], row["type"], row["description"],
					self._list_relation("Event_Resource", DbResource, "event", _id, "resource"),
					self._list_relation("Event_User", DbUser, "event", _id, "user"),
					self._convert_sql_id(row["agenda"], DbAgenda))
		if type is DbGroup:
			return DbGroup(_id, self, row["name"],
					self._list_relation("Group_Admin", DbUser, "group", _id, "admin"),
					self._list_relation("Group_User", DbUser, "group", _id, "user"),
					self._list_id(DbAgenda, "group", _id),
					self._list_id(DbResource, "group", _id))
		if type is DbUser:
			return DbUser(_id, self, row["first_name"], row["last_name"], row["email"], row["tel"],
			   list(self._list_id(DbAgenda, "user", _id))[0],
			   self._list_relation("Group_User", DbGroup, "user", _id, "group"),
			   self._convert_sql_id(row["account"], DbAccount))
		if type is DbNotification:
			return DbNotification(_id, self,
					self._convert_sql_id(row["event"], DbEvent),
					self._convert_sql_id(row["agenda"], DbAgenda),
					row["status"])

	def _load_batched(self, type, attr, value, close):
		_type = self._translate_type(type)

		rows = self._get_row_attr(attr, value, _type.db_table, close)

		datas = set()
		category = self._datas[_type]
		# Conversion de toutes les données.
		for row in rows:
			_id = row["id"]
			data = category.get(_id, None)
			# On ne converti que les données non chargées.
			if data is None:
				data = self._load(_id, _type, row)
				category[_id] = data

			datas.add(data)

		return datas

############ Interface Collection ##############

	def new(self, type, *args):
		_type = self._translate_type(type)
		data = _type(-1, self, *args)
		self.new_queue.add(data)

		return data

	def load(self, proxy):
		_type = self._translate_type(proxy.data_type)
		_id = proxy.id

		# Recherche dans le cache
		category = self._datas[_type]
		data = category.get(_id, None)

		if data is None:
			row = self._get_row(_id, _type.db_table)[0]
			data = category[_id] = self._load(_id, _type, row)

		proxy._data = data

	def load_events(self, agenda, from_date, to_date):
		""" Charge les événements débutant entre deux dates. """
		return self._load_batched(DbEvent, "agenda", agenda.id,
			"AND (start >= \"{}\" AND start < \"{}\")".format(
				from_date, to_date))

	def load_last_events(self, agenda, from_date, to_date):
		""" Charge les événements créés ou midifiés entre deux dates. """
		return self._load_batched(DbEvent, "agenda", agenda.id,
			"AND (creation_date >= \"{}\" AND creation_date < \"{}\")".format(from_date, to_date))

	def load_account(self, login, mdp):
		rows = self._get("SELECT * FROM Account WHERE `login` = \"{}\" AND `mdp` = \"{}\"".format(login, mdp))

		if len(rows) == 0:
			raise ValueError("Invalid account")

		# Premier compte.
		row = rows[0]

		_id = row["id"]

		category = self._datas[DbAccount]
		data = category.get(_id, None)

		if data is None:
			data = category[_id] = self._load(row["id"], DbAccount, row)

		return data

	def load_groups(self, sub_name):
		""" Obtention des groups avec sub_name inclus dans leur nom. """
		return self._list_id_close(DbGroup, "name REGEXP '({})+'".format(sub_name))

	def delete(self, data, delete_proxies):
		_type = self._translate_type(data.data_type)
		self.delete_queue.add(data)

		if data.id != -1:
			# Désenregistrement de la donnée.
			self._unregister_data(data)

			if delete_proxies:
				proxies = _type.db_delete_proxies(self, data.id)
				self._delete_proxies(proxies)

				return proxies

		return set()

	def delete_proxy(self, proxy, delete_proxies):
		_type = self._translate_type(proxy.data_type)
		self.delete_queue.add(proxy)
		# Désenregistrement du proxy.
		self._unregister_proxy(proxy)

		if delete_proxies:
			proxies = _type.db_delete_proxies(self, proxy.id)
			self._delete_proxies(proxies)

			return proxies

	def update(self, data):
		self.update_queue.add(data)

	def update_relations(self, data):
		self.update_relations_queue.add(data)

##############################################

	def flush(self):
		""" "Commit" les modifications """

		def priority(_type):
			""" Calcul de l'ordre d'ecriture par un numéro de priorité.
			Ceci dans le but d'écrire les données en dépendance après leur
			dépendance. Par exemple écrire en premier les agendas avant leur
			événement pour connaitre l'id de l'agenda à utiliser dans l'événement
			"""
			if _type is DbAccount:
				return 1
			if _type in (DbUser, DbGroup):
				return 2
			if _type in (DbAgenda, DbResource):
				return 3
			if _type is DbEvent:
				return 4
			if _type is DbNotification:
				return 5

			raise TypeError()

		""" Ordre :
		Insert
		Update
		Delete

		Pour chaque étape on procède aux entités avant leur relations.
		"""

		# Tri par dépendance.
		new_queue = sorted(self.new_queue, key=lambda item: priority(item.data_type))
		for data in new_queue:
			self._delayed_new(data)

		# Pas de tri pour les relations car toutes les id existent.
		for data in self.new_queue:
			self._delayed_new_relation(data)

		for data in self.update_queue:
			self._delayed_update(data)

		# Il est parfois necessaire de modifier que les relations et non les entitées.
		for data in self.update_relations_queue:
			self._delayed_update_relation(data)

		for data in self.delete_queue:
			self._delayed_delete(data.data_type, data.id)

		self.new_queue.clear()
		self.update_queue.clear()
		self.delete_queue.clear()
