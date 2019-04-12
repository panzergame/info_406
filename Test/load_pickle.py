import pickle

class Proxy:
	def __init__(self, id):
		self.id = id

class Data:
	def __init__(self, id, attrs):
		self.id = id
		self.attrs = attrs

with open("data.pyk", "rb") as file:
	d = pickle.load(file)
	print(d, d.id, d.attrs, [attr.id for attr in d.attrs])
