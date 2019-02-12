from .data import *

class Slot(Data): # TODO ne pas mettre en Data -> exception dans les collections
	def __init__(self, date, start, end):
		self.date = date
		self.start = start
		self.end = end

	@property
	def duration(self):
		return self.end - self.start

	def __repr__(self):
		return "{}:{}({})".format(self.start, self.end, self.duration)
