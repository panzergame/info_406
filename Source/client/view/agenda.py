# -*- coding: utf-8 -*-

import cairo
from datetime import *

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .observer import *
from core import *

from client.controller.agenda import *
from .link_button import LinkButton

class AgendaBox(Gtk.VBox):
	#Affichage d'une semaine d'un agenda, en commençant par le jour passé au constructeur
	def __init__(self, common):
		super().__init__()
		eventBox = Gtk.EventBox()

		self.overlay = Gtk.Overlay()
		#Widget permettant de superposer d'autres widget
		
		self.overlay.add(AgendaTimeAnnotations(common))
		#Ajout du fond de l'agenda, séparateurs de jours et d'heures

		self.agenda_events = AgendaEvents(common)
		self.overlay.add_overlay(self.agenda_events)
		#Ajout des évènements de l'agenda

		self.overlay.add_overlay(AgendaDayAnnotations(common))
		
		eventBox.add(self.overlay)
		self.add(eventBox)

		#Prise en charge des évènements
		listener = AgendaClickListener(common)
		self.connect("button_press_event",listener.manageClick)
	

class AgendaEvents(Gtk.DrawingArea, ViewObserver):
	#Classe d'affichage des évènement d'un agenda
	def __init__(self, common):
		Gtk.DrawingArea.__init__(self)
		ViewObserver.__init__(self, common, common.day, common.agenda_displayed, common.notification_clicked, common.event_clicked, common.users_filtered, common.resources_filtered)

		self.presence = Presence(set(), set())

		def draw(da, ctx):
			""" Fonction appelée à chaque fois que les évènements doivent être dessinés """

			now, start, end = self.date_range()
			events = self.events(start, end)
			notif = self.notification(start, end)
			slots = self.presence.slots(start, end)
			selected_event = self.common.event_clicked.value.get(self.common.agenda_displayed.value, None)

			AgendaEvents.drawEventsAndSlots(da, ctx, events, slots, now)
			if notif is not None:
				AgendaEvents.drawEvent(da, ctx, notif.event, now, (1, 1, 1, 0.5))

			if selected_event is not None:
				AgendaEvents.drawSelectedEvent(da, ctx, selected_event, now)


		self.connect('draw', draw)

	def date_range(self):
		""" Renvoie le jour actuelle, le lundi de la semaine actuelle
		et le lundi de la semaine prochaine. """
		now = self.common.day.value
		start = now - timedelta(days=now.weekday())
		end = now + timedelta(days=7)

		return now, start, end

	def events(self, start, end):
		""" Récupère les événements de l'agenda courant sur une période. """
		ag = self.common.agenda_displayed.value
		if ag is not None:
			return ag.all_events(start, end)
		else:
			return set()

	def notification(self, start, end):
		""" Récupère la notification selectionné si elle se trouve dans une période. """
		notif = self.common.notification_clicked.value
		if notif is not None:
			if notif.event.intersect_range(start, end):
				return notif

		return None

	def update(self):
		group = self.common.group_clicked.value
		if group is not None:
			self.presence = Presence(self.common.users_filtered.value.get(group, set()),
							self.common.resources_filtered.value.get(group, set()))
		else:
			self.presence = Presence(set(), set())

		self.queue_draw()

	@staticmethod
	def drawEventsAndSlots(drawingArea, context, events, slots, firstDay):
		"""Méthode appelant la méthode dessinant un event sur chaque event de l'agenda"""
		
		size = (drawingArea.get_allocation().width, drawingArea.get_allocation().height)
		#On récupère la taille de la zone d'affichage de l'agenda
		
		context.scale(size[0], size[1])
		#On met à l'échelle le contexte dans lequel on va dessiner
		
		for event in events:
			color = ((event.start.hour/24),(event.start.day/30),(event.start.month/12), 1)
			#todo mettre une vraie sélection de couleur, actuellement dépend de la date
			
			context.set_font_size((1/2)*(1/24))
			#La taille des textes est la moitié de l'espace occupé verticalement par une heure
			
			AgendaEvents.drawEvent(drawingArea, context, event, firstDay, color)

		for slot in slots:
			color = (1, 0, 0, 0.5)
			AgendaEvents.drawSlot(drawingArea, context, slot, firstDay, color)

	@staticmethod
	def getSlotCoords(start, end, firstDay):
		"""Permet de récupérer les coordonnées et dimension d'un créneau de l'EDT"""
		minutesPerDay = 24*60
		daysDisplayed = 7

		def toDayMinutes(date):
			"""Permet de connaître le nombre de minutes d'un datetime ou un timedelta sans prendre en compte les jours"""
			if type(date) == datetime:
				return date.minute + date.hour*60
			elif type(date) == timedelta:
				#Temps en secondes
				return (date.seconds/60)
			else:
				raise ValueError

		rectanglesList=[]
		currentStart = start
		for i in range(end.day-start.day+1):
			#On donne les coordoonées du rectangle
			x = (currentStart-firstDay).days*(1/daysDisplayed)
			y = (toDayMinutes(currentStart)/(minutesPerDay))
			width = (1/daysDisplayed)
			
			if currentStart.day==end.day:
				#Si on est le même jour on trace une hauteur qui correspond à la durée de l'évèneme,t
				height = (toDayMinutes(end - currentStart)/(minutesPerDay))
			else:
				#Sinon on trace une hauteur jusqu'à la fin de la journée = complémentaire du temps écoulé depuis le début de la journée
				height = 1-(toDayMinutes(currentStart)/(minutesPerDay))

			#On ajoute le rectangle à tracer à la liste des rectangles
			rectanglesList.append((x,y,width,height))

			#Si l'event s'étend sur plusieurs jours, on recommence en avançant la date de départ de 1 jour, en fonction de ce qui a été tracé
			currentStart=datetime(currentStart.year,currentStart.month,currentStart.day)+timedelta(1)

		return rectanglesList

	@staticmethod
	def drawEvent(drawingArea, context, event, firstDay, color):
		"""Méthode permettant de dessiner un évènement"""

		def drawEventInfo(drawingArea, context, event_rectangle, color):
			"""Permet de dessiner les informations d'un évènement au bon endroit"""
			hours_displayed=24
			display_area_x,display_area_y,display_area_width,display_area_height=event_rectangle[0],event_rectangle[1],event_rectangle[2],event_rectangle[3]

			if(sum(color)>1.5):
			#Test de si la couleur de l'event est claire ou foncée pour une couleur de texte opposée
				color = (0,0,0)
			else:
				color = (1,1,1)
			context.set_source_rgb(color[0],color[1],color[2])

			#Calcul des coordonnées du texte affichant le type de l'event
			event_type_text = event.type

			type_xbearing, type_ybearing, event_text_width, event_text_height, event_text_dx, event_text_dy = context.text_extents(event_type_text)
			#Obtention de la taille d'affichage du texte

			x_event_type = display_area_x + (display_area_width-event_text_width)/2
			y_event_type = display_area_y + (display_area_height-event_text_height)/2
			#On centre le texte dans le carré représentant l'event en x et on le décale un peu en y
					
			context.move_to(x_event_type,y_event_type)
			context.show_text(event_type_text)
			#Affichage du texte

			#Calcul des coordonnées du texte affichant la durée de l'event
			event_duration_text = "{:02d}h{:02d}-{:02d}h{:02d}".format(event.start.hour, event.start.minute, event.end.hour, event.end.minute)

			duration_xbearing, duration_ybearing, event_duration_width, event_duration_height, event_duration_dx, event_duration_dy = context.text_extents(event_duration_text)
			#Obtention de la taille d'affichage du texte

			x_event_duration = display_area_x + (display_area_width-event_duration_width)/2
			y_event_duration = y_event_type + 1/(2*hours_displayed) #Décalage de 30min par rapport à l'affichage du type de l'event
			#coordonnées d'affichage du texte
		
			context.move_to(x_event_duration, y_event_duration)
			context.show_text(event_duration_text)
			#affichage du texte

		#Affichage d'un rectangle de couleur pour l'event
		for event_rectangle in AgendaEvents.getSlotCoords(event.start, event.end, firstDay):
			x, y, width, height = event_rectangle
			context.set_source_rgba(*color)
			context.rectangle(x, y, width, height)
			context.fill()
			#Affichage des infos de l'event sur ce rectangle
			drawEventInfo(drawingArea, context, event_rectangle, color)
			context.fill()

	@staticmethod
	def drawSelectedEvent(drawingArea, context, event, firstDay):
		for x, y, width, height in AgendaEvents.getSlotCoords(event.start, event.end, firstDay):
			AgendaEvents.drawInnerBorder(drawingArea,context,x,y,width,height,(0,0,0),0.005)
			AgendaEvents.drawInnerBorder(drawingArea,context,x,y,width,height,(1,1,1),0.004)
			AgendaEvents.drawInnerBorder(drawingArea,context,x,y,width,height,(0,0,0),0.001)
			#Pour faire une bande blanche aux bords noirs 
			

	@staticmethod
	def drawSlot(drawingArea, context, slot, firstDay, color):
		daysDisplayed = 7

		#Affichage d'un rectangle de couleur pour l'event
		for x, y, width, height in AgendaEvents.getSlotCoords(slot.start, slot.end, firstDay):
			context.set_source_rgba(*color)
			context.rectangle(x, y, width, height)
			context.fill()

	@staticmethod
	def drawInnerBorder(drawingArea, context, x, y, width, height, color, border_width):
		"""Fonction qui permet de tracer une bordure intérieure d'un rectangle"""
		context.set_source_rgb(*color)
		context.set_line_width(border_width)
		context.rectangle(x+border_width/2,y+border_width/2,width-border_width,height-border_width)
		#Quand on trace le contour d'un rectangle avec pycairo, le "milieu" de la bordure correspond au coordonnées du rectangle
		#le calcul effectué sur les coordonnées permet de dessiner une bordure "intérieure" au rectangle auquel on ajout la bordure
		context.stroke()

class AgendaDayAnnotations(Gtk.DrawingArea, ViewObserver):
	"""
	Zone de dessin qui affiche le nom des jours et les traits de séparation entre les jours
	"""
	def __init__(self, common):
		Gtk.DrawingArea.__init__(self)
		ViewObserver.__init__(self, common, common.day)
		self.day = common.day.value
		self.hours_displayed = common.hours_displayed.value
		self.days_displayed = common.days_displayed.value

		self.set_property("expand",True)
		self.connect('draw', self.draw)
		self.show_all()
	
	def draw(self, drawingArea, context):
		"""
		Dessine les annotations de jour
		"""
		###########################
		#initialisation du contexte
		###########################

		size = (drawingArea.get_allocation().width, drawingArea.get_allocation().height)
		context.scale(size[0], size[1])
		#Mise à l'échelle du contexte
		
		context.select_font_face("Purisa")
		#Choix de la police d'écriture

		dashes=[1,0]
		context.set_dash(dashes)
		#On enlève les pointillés potentiels
			
		context.set_line_width(0.001)
		#Taille des lignes tracées

		context.set_font_size(((1/2)*(1/self.hours_displayed)))
		#La hauteur du texte est la même que la hauteur d'une demi-heure dans l'agenda

		context.set_source_rgb(0.2,0.2,0.2)
		#Taille de police et couleur

		###########################
		#Traçage des lignes séparant les jours et de date/nom pour chaque jour
		###########################

		for i in range(0, self.days_displayed):
			#Affichage de la date en haut de chaque colonne correspondant à un jour
			#On choisit la position de départ pour que le texte soit centré

			day_text =  AgendaDayAnnotations.dayToString(self.day+timedelta(days=i))
			xbearing, ybearing, text_width, text_height, dx, dy = context.text_extents(day_text)
			#On récupère la taille que fera le texte

			display_area_width = 1/self.days_displayed
			display_area_height = 1/self.hours_displayed
			#Taille de la zone où on affiche le texte

			display_area_x = display_area_width*i
			display_area_y = (1/2)*(1/self.hours_displayed)
			#On affiche le texte sur la première demi-heure de la journée

			text_x_offset = (display_area_width - text_width)/2
			#Décalage du texte par rapport à la zone d'affichage pour que le texte soit centré en x

			context.move_to(display_area_x + text_x_offset, display_area_y + 0)
			context.show_text(day_text)

		for i in range(1, self.days_displayed):
			#Traçage des lignes verticales séparant les jours
			context.move_to(i/(self.days_displayed), 0)
			context.line_to(i/(self.days_displayed), 1)
	
		context.stroke()
		#Application des changements

	def update(self):
		"""méthode appelée lorsque le modèle change"""
		self.queue_draw()

	@staticmethod
	def dayToString(current_day):
		day_num = current_day.weekday()
		if day_num == 0:
			dayName="lun"
		elif day_num == 1:
			dayName="mar"
		elif day_num == 2:
			dayName="mer"
		elif day_num == 3:
			dayName="jeu"
		elif day_num == 4:
			dayName="ven"
		elif day_num == 5:
			dayName="sam"
		elif day_num == 6:
			dayName="dim"

		return ("{} {:02d}/{:02d}".format(dayName, current_day.day, current_day.month))

class AgendaTimeAnnotations(Gtk.DrawingArea, ViewObserver):
	"""Classe de dessin des annotations de temps"""
	def __init__(self, common):
		Gtk.DrawingArea.__init__(self)
		ViewObserver.__init__(self, common, common.day)

		self.hours_displayed = common.hours_displayed.value
		self.days_displayed = common.days_displayed.value

		self.set_property("expand",True)
		self.connect('draw', self.draw)
		self.show_all()

	def draw(self, drawingArea, context):
		#Méthode qui trace les annotations

		#################################
		#Intialisation du contexte
		#################################

		size = (drawingArea.get_allocation().width, drawingArea.get_allocation().height)
		context.scale(size[0], size[1])
		#Mise à l'échelle du contexte
		
		context.set_source_rgb(0.8, 0.8, 0.8)
		context.rectangle(0, 0, 1, 1)
		context.fill()
		
		context.select_font_face("Purisa")
		#Choix de la police d'écriture
		
		context.set_line_width(0.002)
		#épaisseur des lignes tracées

		dashes_width = 1/(self.days_displayed*10)
		dashes=[dashes_width,dashes_width]
		context.set_dash(dashes)
		#Permet d'afficher un trait pointillé avec 5 répétitions de motif par jour affiché
			
		context.set_font_size((1/3)*(1/self.hours_displayed))
		context.set_source_rgb(0.5, 0.5, 0.5)
		#Taille de police et couleur

		##############################
		#Tracage des annotations
		#############################
			
		for i in range(1, self.hours_displayed):
			#Pour chaque heure
				
			context.move_to(0.002, (i/self.hours_displayed)-0.002)
			context.show_text("{}h".format(i))
			#On se place un peu au dessus de la ligne à tracer et on écrit l'heure
				
			context.move_to((dashes_width/2), i/self.hours_displayed)
			#(dashes_width/2) correspond au décalage de départ du trait pointillé
			context.line_to(1, i/self.hours_displayed)
			#On trace les pointillés

		context.stroke()
		#Traçage des lignes correspondant aux heures

	def update(self):
		"""méthode appelée lorsque le modèle change"""
		self.queue_draw()
