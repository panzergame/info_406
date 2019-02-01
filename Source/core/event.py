class Event:
	def __init__(self, slot, type, description):
		self.slot = slot
		self.type = type
		self.description = description

	def __repr__(self):
		return "{} {}".format(self.type, self.slot)
