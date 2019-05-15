class ViewObserver:
	""" Un observateur du changement de l'état de la vue
		e.g un événement clické, un agenda affiché…"""

	def __init__(self, common, *args):
		self.common = common

		for observable in args:
			observable.register(self)
