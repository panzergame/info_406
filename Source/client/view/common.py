# -*- coding: utf-8 -*-

""" Outils de conversion commun pour la vue. """

def get_or_init(d, key, init):
	if key in d:
		d[key]
	else:
		d[key] = init
	return d[key]

def datetime_str(date):
	return date.strftime("%d/%m/%Y à %H:%M")

def date_to_day_str(date):
	return date.strftime("%d/%m/%Y")

def date_to_hour_str(date):
	return date.strftime("%H:%M")

def event_to_date_str(start, end):
	""" Conversion de la date et heure d'un événement en une chaine. """

	start_hour = date_to_hour_str(start)
	end_hour = date_to_hour_str(end)

	# Test si les deux dates sont le même jour.
	if start.toordinal() == end.toordinal():
		return "{} de {} à {}".format(start.strftime("%d/%m/%Y"), start_hour, end_hour)

	return "{} {} à {} {}".format(start.strftime("%d/%m/%Y"), start_hour, end.strftime("%d/%m/%Y"), end_hour)
