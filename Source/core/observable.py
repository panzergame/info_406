# -*- coding: utf-8 -*-

class Observable:
	""" Une instance observable """
	def __init__(self):
		self._observers = set()

	def register(self, obs):
		self._observers.add(obs)

	def unregister(self, obs):
		self._observers.discard(obs)

	def notify(self):
		for obs in self._observers.copy():
			obs.update()

class ObservableAttribute(Observable):
	def __init__(self, value):
		super().__init__()
		self._value = value

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, v):
		self._value = v
		self.notify()

class NotifyingDict(dict):
	"""Un dictionnaire qui peut appeler une méthode (ici, notify) quand une des ses clés changent de valeur"""
	def __init__(self, notify_method):
		self.notify = notify_method

	def set_to_dict(self, d):
		for key in d.keys():
			self[key] = d[key]

	def __setitem__(self, key, value):
		super().__setitem__(key, value)
		self.notify()

class ObservableDict(ObservableAttribute):
	"""Un attribut observable de type dictionnaire, qui notify la vue à chaque clé modifiée"""
	def __init__(self):
		super().__init__(NotifyingDict(self.notify))

	@property
	def value(self):
		return super().value

	@value.setter
	def value(self, d):
		self.value.set_to_dict(d)
		self.notify()