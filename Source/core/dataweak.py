# -*- coding: utf-8 -*-

class WeakRefSet:
	""" Un ensemble d'élément se supprimant de l'ensemble lors de leur destruction.

		Par exemple la suppression d'un utilisateur doit prevenir le compte de le retirer
		de sa liste d'utilisateur.

		Si cette ensemble à un propriétaire (owner) alors il peut lui appeler sa méthode
		update_relations pour lui notifier qu'une de ses ensembles a changé.
	"""

	def __init__(self, items=set(), owner=None):
		self.owner = owner
		self._set = set(items)

		self._weakrefs = set()
		
		for item in self._set:
			item.new_ref(self)

	def _update_owner(self):
		if self.owner is not None:
			self.owner.update_relations()

	def __iter__(self):
		return self._set.__iter__()

	def __repr__(self):
		return self._set.__repr__()

	def __len__(self):
		return self._set.__len__()

	def __ior__(self, other):
		if type(other) == set:
			for item in other:
				item.new_ref(self)

			self._set |= other
			self._update_owner()
		elif type(other) == WeakRefSet:
			for item in other._set:
				item.new_ref(self)

			self._set |= other._set
			self._update_owner()
		else:
			raise TypeError()

		return self

	def __rsub__(self, other):
		if type(other) == set:
			return other - self._set
		elif type(other) == WeakRefSet:
			return other._set - self._set
		else:
			raise TypeError()

	def __isub__(self, other):
		if type(other) == set:
			removed = self._set - other
		elif type(other) == WeakRefSet:
			removed = self._set - other._set
		else:
			raise TypeError()

		for item in removed:
			item.del_ref(self)

		self._set -= other

		return self

	def delete(self, owner=None, delete_proxies=False):
		self._update_owner()
		for ref in self._weakrefs:
			ref.delete(owner=self, delete_proxies=False)
		return self.discard(owner, del_ref=False)

	def discard(self, item, del_ref=True):
		self._update_owner()
		if del_ref:
			item.del_ref(self)
		return self._set.discard(item)

	def add(self, item):
		item.new_ref(self)
		return self._set.add(item)

	def new_ref(self, ref):
		#print("new ref", self, ref, type(ref))
		self._weakrefs.add(ref)

	def del_ref(self, ref):
		#print("del ref", self, ref, type(ref))
		self._weakrefs.discard(ref)

class WeakRefered:
	""" Une classe pouvant prevenir des référents de sa destruction,
		les référents doivent s'enregistrer avec new_ref.
		
		Cette methode est appelé que par DataOwnerProperty et WeakRefSet
		et ne doit pas être utilisé ailleur.
	"""

	def __init__(self):
		""" Utilisation d'un weak ref set pour que ne pas garder en référence un objet supprime.
		Par exemple chaque événement d'un agenda s'enregistre au près de cette agenda pour lorsque
		l'agenda soit supprimé les événements le soit aussi.
		
		Mais si l'on supprime un événement et que ensuite on supprime l'agenda il faut éviter que l'agenda
		essaye de supprimer l'événement que l'on viens juste de supprimer
		"""

		self._weakrefs = WeakRefSet()

	def new_ref(self, ref):
		""" Ajout d'une reférence, ref sera notifier de la destruction. """
		#print("new ref", self, ref, type(ref))
		self._weakrefs.add(ref)

	def del_ref(self, ref):
		""" Suppression d'une référence, ref ne sera plus notifier de la destruction. """
		#print("del ref", self, ref, type(ref))
		self._weakrefs.discard(ref)

	def delete(self):
		""" Suppression et notification des référents """
		#print("delete refs", self._weakrefs, "from", self)
		for ref in set(self._weakrefs):
			ref.delete(owner=self, delete_proxies=False)
