# -*- coding: utf-8 -*-

from core import *
from datetime import datetime

class Common:
	def __init__(self, collection):
		self.is_connected = ObservableAttribute(False)
		self.has_account = ObservableAttribute(True)
		self.user_clicked = ObservableAttribute(None)
		self.group_clicked = ObservableAttribute(None)
		self.agenda_displayed = ObservableAttribute(None)
		self.account = ObservableAttribute(None)
		self.day = ObservableAttribute(datetime.now())
		self.event_clicked = ObservableAttribute({})
		self.notification_clicked = ObservableAttribute(None)
		self.users_filtered = ObservableAttribute({})
		self.resources_filtered = ObservableAttribute({})
		self.hours_displayed=ObservableAttribute(24)
		self.days_displayed=ObservableAttribute(7)
		self.collection = collection


	def notify(self):
		self.is_connected.notify()
		self.has_account.notify()
		self.user_clicked.notify()
		self.group_clicked.notify()
		self.agenda_displayed.notify()
		self.account.notify()
		self.day.notify()
		self.event_clicked.notify()
		self.notification_clicked.notify()
