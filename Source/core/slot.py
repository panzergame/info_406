from .data import *

class Slot(Data):
	def __init__(self, id, date, start, duration):
		super().__init__(id)

		self.date = date
		self.start = start
		self.duration = duration

	@property
	def end(self):
		return self.start + self.duration

	def __repr__(self):
		return "{} {}:{}({})".format(self.date, self.start, self.end, self.duration)
