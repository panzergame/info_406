import pickle

class Proxy:
	def __init__(self, id):
		self.id = id

class Data:
	def __init__(self, id, attrs):
		self.id = id
		self.attrs = attrs

p1 = Proxy(1)
p2 = Proxy(2)

d = Data(3, {p1, p2})

with open("data.pyk", "wb") as file:
	pickle.dump(d, file)
