#############################################################""
# Fichier contenant les classes qui servent à manipuler les données utilisées par
# le dialogue de gestion des permissions des membres d'un groupe

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

	def to_admin(self, member):
		self.member_to_admin.add(member)

	def stay_member(self, member):
		self.member_to_admin.remove(member)

	def to_member(self, admin):
		self.admin_to_member.add(admin)

	def stay_admin(self, admin):
		self.admin_to_member.remove(admin)

	def get_admin_search_results(self):
		pass
		#return self.collection.load_members_by_name_from_group()

	def get_member_search_results(self, name):
		pass
		#return self.collection.load_admins_by_name_from_group()

	def apply_changes(self):
		#Inscription des changements dans la BDD
		pass