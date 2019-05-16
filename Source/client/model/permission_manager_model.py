#############################################################""
# Fichier contenant les classes qui servent à manipuler les données utilisées par
# le dialogue de gestion des permissions des membres d'un groupe

import re

class PermissionManagerModel():
	def __init__(self, collection, group):
		self.collection = collection
		self.group = group
		self._admin_search = ""
		self._member_search = ""
		self._member_to_admin = set()
		self._admin_to_member = set()
		self.observers = set()

	def add_observer(self, obs):
		self.observers.add(obs)

	def notify(self):
		for obs in self.observers:
			obs.update(self)

	@property
	def member_to_admin(self):
		return self._member_to_admin

	@property
	def admin_to_member(self):
		return self._admin_to_member

	@property
	def admin_search(self):
		return self._admin_search
	
	@admin_search.setter
	def admin_search(self, admin_name):
		self._admin_search = admin_name
		self.notify()

	@property
	def member_search(self):
		return self._member_search

	@member_search.setter
	def member_search(self, member_name):
		self._member_search = member_name
		self.notify()

	def get_admin_search_results(self):
		results = set()
		search = self.admin_search
		pattern = re.compile("({})+".format(search),flags=re.IGNORECASE)
		#TODO union
		for admin in self.group.admins:
			if(pattern.search(admin.first_name) or pattern.search(admin.last_name)):
				results.add(admin)
		return results

	def get_member_search_results(self):
		results = set()
		search = self.member_search
		pattern = re.compile("({})+".format(search),flags=re.IGNORECASE)
		#TODO utiliser la soustraction de set de manière conventionnelle
		for member in (self.group.admins.__rsub__(self.group.subscribers)):
			if(pattern.search(member.first_name) or pattern.search(member.last_name)):
				results.add(member)
		return results

	def apply_changes(self):
		#Inscription des changements 
		for member in self.member_to_admin:
			self.group.add_admin(member)
		
		for admin in self.admin_to_member:
			self.group.remove_admin(admin)

