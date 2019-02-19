# -*- coding: utf-8 -*-

class Presence:
	def __init__(self, slot, users):
		self.slot = slot
		self.users = users

	def __repr__(self):
		return "{} : {}".format(self.slot, self.users)
