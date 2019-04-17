# -*- coding: utf-8 -*-

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from server import *
from core import *
from .db_open import *

with SimpleXMLRPCServer(('localhost', 8000), allow_none=True, use_builtin_types=True) as server:
    server.register_instance(Server(collection))

    # Run the server's main loop
    server.serve_forever()
