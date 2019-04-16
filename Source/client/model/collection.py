# -*- coding: utf-8 -*-

from server import *

import xmlrpc.client

# TEMP
import xml.etree.ElementTree as ET

tree = ET.parse("config.xml")
root = tree.getroot()

login = root.find("login").text
password = root.find("password").text
server = root.find("server").text
# TEMP

class ClientCollection(ServerClientCollection):
	def __init__(self):
		s = xmlrpc.client.ServerProxy('http://localhost:8000', use_builtin_types=True)

		super().__init__(s)
	
