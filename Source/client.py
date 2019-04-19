# -*- coding: utf-8 -*-

from client import *
from core import *
from db import *

#import xmlrpc.client

#s = xmlrpc.client.ServerProxy('http://localhost:8000', use_builtin_types=True)

#collection = ClientCollection(s)

collection = ClientCollection()
common = Common(collection)

win = Window(common)
win.main()

collection.close()
