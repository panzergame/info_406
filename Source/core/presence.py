# -*- coding: utf-8 -*-

class Slot:
	def __init__(self, start, end):
		self.start = start
		self.end = end

	def __repr__(self):
		return "{} to {}".format(self.start, self.end)

class Presence:
	def __init__(self, users, resources):
		self.users = users
		self.resources = resources

	def slots(self, from_date, to_date):
		# On récupère tous les événements de cette période
		all_events = set()

		# Les événements des utilisateurs.
		for user in self.users:
			all_events |= user.agenda.all_events(from_date, to_date)

		# Les événements qui utilise les ressources dans leur groupes.
		for res in self.resources:
			for agenda in res.group.agendas:
				for events in agenda.events(from_date, to_date):
					if res in event.resources:
						all_events.add(event)

		slots = []
		for event in all_events:
			# Les slots en intersection avec cet événement.
			intersected_slots = []
			for slot in slots:
				if event.intersect_wide_range(slot.start, slot.end):
					intersected_slots.append(slot)
	
			# Pas d'intersections
			if len(intersected_slots) == 0:
				slot = Slot(event.start, event.end)
				slots.append(slot)
			# Fusion de tout les slots et de l'événements
			else:
				# On cherche le plus petit debut et plus grande fin parmis les slot en intersection.
				min_slots = min(map(lambda slot : slot.start, intersected_slots))
				max_slots = max(map(lambda slot : slot.end, intersected_slots))

				start = min(min_slots, event.start)
				end = max(max_slots, event.end)

				# On supprime les slot fussionnés.
				for slot in intersected_slots:
					slots.remove(slot)

				# On ajoute le nouveau slot
				slot = Slot(start, end)
				slots.append(slot)

		return slots
