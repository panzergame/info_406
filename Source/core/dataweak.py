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
			ref.delete(self)

class WeakRefSet:
	def __init__(self, owner, items):
		self.owner = owner
		self._set = set(items)
		
		for item in self._set:
			item.new_ref(self)

	def __iter__(self):
		return self._set.__iter__()

	def __repr__(self):
		return self._set.__repr__()

	def __len__(self):
		return self._set.__len__()

	def delete(self, refered):
		self.owner.update_relations()
		return self.discard(refered)

	def discard(self, item):
		self.owner.update_relations()
		return self._set.discard(item)

	def add(self, item):
		return self._set.add(item)
