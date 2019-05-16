# -*- coding: utf-8 -*-

from core import *
from db import *
from datetime import datetime

import mysql.connector
import xml.etree.ElementTree as ET

tree = ET.parse("config.xml")
root = tree.getroot()

login = root.find("login").text
password = root.find("password").text
database = root.find("database").text

conn = mysql.connector.connect(host="localhost", user=login, password=password, database=database)

collection = DbCollection(conn)
