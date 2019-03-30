# -*- coding: utf-8 -*-

from db import *

import mysql.connector

class ClientCollection(DbCollection):
	def __init__(self):
		self.conn = mysql.connector.connect(host="localhost", user="root", password="root", database="info_406")
		self.cursor = self.conn.cursor()

		super().__init__(self.cursor)

	def flush(self):
		self.conn.commit()

	def close(self):
		self.cursor.close()
	
