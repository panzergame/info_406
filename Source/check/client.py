import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000')

toto_session = s.connect("toto", "root")
print("Toto session : ", toto_session)

s.event(0)
