# -*- coding: utf-8 -*-
from datetime import *

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AgendaClickListener():
	
	def __init__(self, common):
		self.common = common
	
	def getDatetimeFromRelativeCoords(x, y, start_datetime, days_displayed, hours_displayed):
		#Renvoie sous forme de datetime le moment de l'endroit cliqué sur l'agenda

		relative_day = int(((x)//(1/days_displayed)))
		#Nb de jours écoulés entre l'endroit cliqué et le premier jour affiché

		click_day_datetime = start_datetime + timedelta(relative_day)
		#Datetime comprenant les informations de l'horaire cliqué, avec une précision jusqu'au jour

		click_year = click_day_datetime.year
		click_month = click_day_datetime.month
		click_day = click_day_datetime.day

		click_hour = int(y*hours_displayed)
		click_minutes = round((y-int(y)) * 60)
		#y-int(y) donne la progression entre l'heure actuelle et l'heure suivante,
		#60 est le nombre de secondes dans une minute
		#On obtient donc le nb de minutes

		click_datetime = datetime(click_year, click_month, click_day, click_hour, click_minutes)
		return click_datetime

	def manageClick(self, widget, event):
		#Gestionnaire du click sur un agenda
		days_displayed = 7
		hours_displayed = 24
		raw_x, raw_y = event.get_coords()
		width, height = widget.get_allocation().width, widget.get_allocation().height
		x, y = (raw_x/width), (raw_y/height)

		clicked_time = AgendaClickListener.getDatetimeFromRelativeCoords(x, y, self.common.day, days_displayed, hours_displayed)

		for event in self.common.user_clicked.agenda.all_events:
			if event.start < clicked_time < event.end:
				self.common.event_clicked = event
		

		
			