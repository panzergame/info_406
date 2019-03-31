# -*- coding: utf-8 -*-

from core import user
from datetime import datetime

class Common:
	def __init__(self, collection):
		self._user_clicked = None
		self._agenda_displayed = None
		self._account = None
		self._day = datetime.now()
		self._event_clicked = None
		self._current_search_text=""
		self.collection = collection
		self.observers = set()

	def add_observer(self, observer):
		self.observers.add(observer)

	def _notify(self):
		for obs in self.observers:
			obs.update(self)

	@property
	def account(self):
		return self._account

	@account.setter
	def account(self, account):
		self._account = account
		self._notify()

	@property
	def user_clicked(self):
		return self._user_clicked

	@user_clicked.setter
	def user_clicked(self, user):
		self._user_clicked = user
		self._notify()

	@property
	def agenda_displayed(self):
		return self._agenda_displayed

	@agenda_displayed.setter
	def agenda_displayed(self, user):
		self._agenda_displayed = user
		self._notify()

	@property
	def event_clicked(self):
		return self._event_clicked

	@event_clicked.setter
	def event_clicked(self, event):
		self._event_clicked = event
		self._notify()

	@property
	def day(self):
		return self._day

	@day.setter
	def day(self, day):
		self._day = day
		self._notify()

	@property
	def current_search_text(self):
		return self._current_search_text

	@current_search_text.setter
	def current_search_text(self, current_search_text):
		self._current_search_text = current_search_text
		self._notify()
