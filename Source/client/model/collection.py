# -*- coding: utf-8 -*-

from db import *

import mysql.connector

# TEMP
import xml.etree.ElementTree as ET

tree = ET.parse("config.xml")
root = tree.getroot()

login = root.find("login").text
password = root.find("password").text
database = root.find("database").text
# TEMP

class ClientCollection(DbCollection):
	def __init__(self):
		self.conn = mysql.connector.connect(host="localhost", user=login, password=password, database=database)

		super().__init__(self.conn)

	def flush(self):
		self.conn.commit()

	def close(self):
		self.cursor.close()
	
