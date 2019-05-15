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
