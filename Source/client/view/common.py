# -*- coding: utf-8 -*-

""" Outils de conversion commun pour la vue. """

def date_to_hour_str(date):
	return "{:02d}:{:02d}".format(date.hour, date.minute)

def event_to_date_str(start, end):
	""" Conversion de la date et heure d'un événement en une chaine. """

	start_hour = date_to_hour_str(start)
	end_hour = date_to_hour_str(end)

	# Test si les deux dates sont le même jour.
	if start.toordinal() == end.toordinal():
		return "{} de {} à {}".format(start.strftime("%d/%m/%Y"), start_hour, end_hour)

	return "{} {} à {} {}".format(start.strftime("%d/%m/%Y"), start_hour, end.strftime("%d/%m/%Y"), end_hour)
