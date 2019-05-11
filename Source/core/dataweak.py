# -*- coding: utf-8 -*-

class WeakRefered:
	def __init__(self):
		self._weakrefs = []

	def new_ref(self, ref):
		#print("new ref")
		self._weakrefs.append(ref)

	def del_ref(self, ref):
		#print("del ref")
		self._weakrefs.remove(ref)

	def delete(self):
		#print("delete refs")
		for ref in self._weakrefs:
			ref.delete(owner=self, delete_proxies=False)

class WeakRefSet:
	def __init__(self, items=set(), owner=None):
		self.owner = owner
		self._set = set(items)
		
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
		return self.discard(owner)

	def discard(self, item):
		self._update_owner()
		item.del_ref(self)
		return self._set.discard(item)

	def add(self, item):
		item.new_ref(self)
		return self._set.add(item)
