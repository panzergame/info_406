from core import *

class DbCollection(Collection):
	def __init__(self, cursor):
		super().__init__()

		self.cursor = cursor

	def _get_row(self, _id, table):
		self.cursor.execute("SELECT * FROM {} WHERE id = {}".format(table, _id))
		return cursor.fetchall()

	def _load_account(self, _id, row):
		pass

	def _load_agenda(self, _id, row):
		pass
		

	def _load_event(self, _id, row):
		pass
		

	def _load_group(self, _id, row):
		pass
		

	def _load_user(self, _id, row):
		pass
		

	def _load(self, _id, type):
		row = self._get_row(_id, type.__name__)

		if type == Account:
			return self._load_account(_id, row)
		if type == Agenda:
			return self._load_agenda(_id, row)
		if type == Event:
			return self._load_event(_id, row)
		if type == Group:
			return self._load_group(_id, row)
		if type == User:
			return self._load_user(_id, row)
			
