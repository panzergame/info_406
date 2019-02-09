import xmlrpc.client

from client import *
from core import *

s = xmlrpc.client.ServerProxy('http://localhost:8000', use_builtin_types=True)

toto_session = s.connect("toto", "root")
print("Toto session : ", toto_session)

collection = ClientCollection(s)

user = collection.load(0, User)
print(user)
agenda = user.agenda
print(agenda)
print(agenda.all_events)
