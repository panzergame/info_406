# -*- coding: utf-8 -*-

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

import mysql.connector

from server import *
from db import *

# TEMP
import xml.etree.ElementTree as ET

tree = ET.parse("config.xml")
root = tree.getroot()

login = root.find("login").text
password = root.find("password").text
database = root.find("database").text
# TEMP

class SessionServer:
	""" Un serveur gérant la création de session et
	redirigant les appelles vers un serveur associé à un
	numéro de session
	"""

	def __init__(self):
		# Session avec un identifiant et un serveur associé.
		self.sessions = {}
		self.last_id = 1

	def new_session(self):
		conn = mysql.connector.connect(host="localhost", user=login, password=password, database=database)

		collection = DbCollection(conn)

		_id = self.last_id
		self.sessions[_id] = Server(collection)
		self.last_id += 1

		return _id

	def end_session(self, id):
		pass # TODO MEURTREEEEE !!!

	def _dispatch(self, name, args):
		if name == "new_session":
			return self.new_session(*args)
		else:
			session_id, *func_args = args

			# Obtention du serveur de la session.
			server = self.sessions[session_id]
			# Appelle de la fonction
			func = getattr(server, name)
			return func(*func_args)

with SimpleXMLRPCServer(('localhost', 8000), allow_none=True, use_builtin_types=True) as server:
    server.register_instance(SessionServer())

    # Run the server's main loop
    server.serve_forever()
