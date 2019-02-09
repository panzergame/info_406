import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000', use_builtin_types=True)

toto_session = s.connect("toto", "root")
print("Toto session : ", toto_session)

user = s.load(0, "User")
print(user)
