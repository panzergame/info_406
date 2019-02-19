# -*- coding: utf-8 -*-

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from server import *
from core import *
from .collection import MyCollection

collection = MyCollection()

with SimpleXMLRPCServer(('localhost', 8000)) as server:
    server.register_instance(Server(collection))

    # Run the server's main loop
    server.serve_forever()
