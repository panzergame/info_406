Agenda
======

.. class:: agenda

  .. method:: new(collection, name)
	 Construction d'un nouveau agenda.

	:param collection: La collection de l'agenda.
	:type collection: Collection
	:param name: Le nom de l'agenda.
	:type name: string
	:return: Un nouveau agenda
	:type return: Agenda

	.. code-block:: python

		# Création de l'agenda nommé "Agenda de Toto"
		agenda = Agenda.new(collection, "Agenda de Toto")

  .. attribute:: name
	 Le nom de l'agenda

	:type: string

  .. attribute:: last_sync
	 Date de la dernière synchronisation

	:type: datetime

  .. attribute:: user
	 Utilisateur propriétaire de l'agenda, peut être None.

	 :type: :class:`User` ou None

  .. attribute:: group
	Groupe propriétaire de l'agenda, peut être None.

	:type: :class:`Group` ou None

	.. code-block:: python

		# Récupération du nom de l'agenda
		agenda.name
		# Modification
		agenda.name = "Agenda de Tata"

		# Dernière synchronisation des notifications
		agenda.last_sync

		# Récupération du propriétaire, un groupe ou un utilisateur
		owner = agenda.user if agenda.user is not None else agenda.group

  .. method:: add_event(event)
	Ajoute un événement.

	:param event: L'événement à ajouter
	:type event: :class:`Event`
  
