class Slot:
	def __init__(self, start, end):
		self.start = start
		self.end = end

	@property
	def duration(self):
		return self.end - self.start

	def __repr__(self):
		return "{}:{}({})".format(self.start, self.end, self.duration)
