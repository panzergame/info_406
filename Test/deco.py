class Prop(property):
	def __init__(self, attr_name):
		hide_attr_name = "_" + attr_name
		def getter(inst):
			return getattr(inst, hide_attr_name)

		def setter(inst, value):
			print(inst, value)
			setattr(inst, hide_attr_name, value)

		super().__init__(getter, setter)

	def __get__(self, instance, owner):
		print(instance, owner)
		return super().__get__(instance, owner)

class A:
	a = Prop("a")

	def __init__(self):
		self._a = 2

	def __setattr__(self, name, value):
		if name[0] == '_':
			object.__setattr__(self, name, value)
		else:
			print("new")
			object.__setattr__(self, name, value)

a = A()
print(a.a)
a.a = 42
