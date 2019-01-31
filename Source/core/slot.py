class Slot:
	def __init__(self, start, duration):
		self.start = start
		self.duration = duration

	@property
	def end(self):
		return self.start + self.duration
