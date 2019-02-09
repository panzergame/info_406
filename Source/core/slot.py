from .data import *

class Slot(Data):
	def __init__(self, _id, date, start, end):
		super().__init__(_id)

		self.date = date
		self.start = start
		self.end = end

	@property
	def duration(self):
		return self.end - self.start

	def __repr__(self):
		return "{}:{}({})".format(self.start, self.end, self.duration)
