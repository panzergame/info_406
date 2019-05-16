from client.model.permission_manager_model import *

class member():
	def __init__(self, f_name, l_name):
		self.first_name = f_name
		self.last_name = l_name

class group():
	def __init__(self, admin_set):
		self.admins = admin_set

admins = set()
admins.add(member("jean","paul"))
admins.add(member("jeanne","paulette"))
admins.add(member("franck","dupont"))
admins.add(member("Paul","Pajeanne"))
admins.add(member("Jean","majuscule"))
admins.add(member("arthur","dupuis"))

pmm = PermissionManagerModel("collection",group(admins))

def print_results(pmm):
	print("\nsearch:{}".format(pmm.admin_search))
	for member in pmm.get_admin_search_results():
		print("{} {}".format(member.first_name, member.last_name))

pmm.admin_search = "jean"
print_results(pmm)

pmm.admin_search = "paul"
print_results(pmm)