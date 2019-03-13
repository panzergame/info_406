# -*- coding: utf-8 -*-

from .core import *

class DbUser(User):
	def __init__(self, *args):
		super().__init__(self, *args)
