from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from server import *
from core import *

# Création d'un utilisateur
user = User("Toto", "Dupont", "toto@mail.com", "0656565656")

with SimpleXMLRPCServer(('localhost', 8000)) as server:
    server.register_instance(Server())

    # Run the server's main loop
    server.serve_forever()
