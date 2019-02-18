# -*- coding: utf-8 -*-

import cairo
from datetime import *

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AgendaBox(Gtk.Box):
    #Affichage d'une semaine d'un agenda, en commençant par le jour passé au constructeur
    def __init__(self, agenda, day):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        overlay = Gtk.Overlay()
        #Widget permettant de superposer d'autres widget
        
        overlay.add(AgendaTimeAnnotations(day))
        #Ajout du fond de l'agenda, séparateurs de jours et d'heures
        
        overlay.add_overlay(AgendaEvents(agenda.all_events, day))
        #Ajout des évènements de l'agenda
        
        self.add(overlay)


class AgendaEvents(Gtk.DrawingArea):
    #Classe d'affichage des évènement d'un agenda
    def __init__(self, events, day):
        
        def draw(da, ctx):
            #Fonction appelée à chaque fois que les évènements doivent être dessinés
            AgendaEvents.drawAllEvents(da, ctx, events, day)
            
        Gtk.DrawingArea.__init__(self)
        self.connect('draw', draw)

    def drawAllEvents(drawingArea, context, events, firstDay):
        #Méthode appelant la méthode dessinant un event sur chaque event de l'agenda
        
        size = (drawingArea.get_allocation().width, drawingArea.get_allocation().height)
        #On récupère la taille de la zone d'affichage de l'agenda
        
        context.scale(size[0], size[1])
        #On met à l'échelle le contexte dans lequel on va dessiner
        
        for event in events:
            color = ((event.start.hour/24),(event.start.day/30),(event.start.month/12))
            #todo mettre une vraie sélection de couleur, actuellement dépend de la date
            
            context.set_font_size((1/2)*(1/24))
            #La taille des textes est la moitié de l'espace occupé verticalement par une heure
            
            AgendaEvents.drawEvent(drawingArea, context, event, firstDay, color)

        
    def drawEvent(drawingArea, context, event, firstDay, color):
        #Méthode permettant de dessiner un évènement
        
        minutesPerDay = 24*60
        daysDisplayed = 7
        
        def toDayMinutes(date):
            #Permet de connaître le nombre de minutes d'un datetime ou un deltatime sans prendre en compte les jours
            if type(date) == datetime:
                return date.minute + date.hour*60
            elif type(date) == timedelta:
                #Temps en secondes
                return (date.seconds/60)
            else:
                raise ValueError
        
        
        def getSlotCoords(start, end, firstDay):
            #Permet de récupérer les coordonnées et dimension d'un créneau de l'EDT
            x = (start-firstDay).days*(1/daysDisplayed)
            y = (toDayMinutes(start)/(minutesPerDay))
            width = (1/daysDisplayed)
            height = (toDayMinutes(end - start)/(minutesPerDay))
            return x, y, width, height

        def drawEventInfo(drawingArea, context, event, color):
            #Permet de dessiner le résumé des informations d'un event
            if(sum(color)>1.5):
            #Test de si la couleur de l'event est claire ou foncée
                color = (0,0,0)
            else:
                color = (1,1,1)

            context.set_source_rgb(color[0],color[1],color[2])

            x_text = x + 0.1*width
            y_text = y + 0.5*height
        
            context.move_to(x_text,y_text)
            context.show_text("{}".format(event.type))
        
            context.move_to(x_text,y_text+1/48)
            #Décalage de 1/2 heure vers le bas par rapport au type de l'event
            context.show_text("{:02d}h{:02d}-{:02d}h{:02d}".format(event.start.hour, event.start.minute, event.end.hour, event.end.minute))
            
            
        context.set_source_rgb(color[0],color[1],color[2])

        #Affichage d'un rectangle de couleur pour l'event
        x, y, width, height = getSlotCoords(event.start, event.end, firstDay)
        context.rectangle(x, y, width, height)
        context.fill()

        #Affichage des infos de l'event sur ce rectangle
        drawEventInfo(drawingArea, context, event, color)
        context.fill()
        
        



class AgendaTimeAnnotations(Gtk.DrawingArea):
    #Classe d'affichage du fond de l'agenda
    def __init__(self, startDay):
        day  = startDay
        def draw(da, ctx):
            AgendaTimeAnnotations.drawAnnotations(da, ctx, day)
            
        Gtk.DrawingArea.__init__(self)
        self.set_property("expand",True)
        self.connect('draw', draw)

    def drawAnnotations(drawingArea, context, startDay):
        #Classe de dessin des annotations de temps
        daysDisplayed = 7
        hoursDisplayed = 24
        def drawTimeLines():
            #Méthode de traçage des lignes correspondant aux heures
            dashes=[(1/70),(1/70)]
            context.set_dash(dashes)
            #Pointillé
            
            context.set_font_size((1/3)*(1/hoursDisplayed))
            context.set_source_rgb(0.5, 0.5, 0.5)
            #Taille de police et couleur
            
            for i in range(1, hoursDisplayed):
                #Pour chaque heure
                
                context.move_to(0.002, (i/hoursDisplayed)-0.002)
                context.show_text("{}h".format(i))
                #On se place un peu au dessus de la ligne à tracer et on écrit l'heure
                
                context.move_to(0, i/hoursDisplayed)
                context.line_to(1, i/hoursDisplayed)
                #On trace la ligne

        def drawDayLines():
            #Méthode de traçage des lignes correspondant aux jours
            dashes=[1,0]
            context.set_dash(dashes)
            #On enlève les pointillés potentiels
            
            context.set_font_size(((1/2)*(1/hoursDisplayed)))
            context.set_source_rgb(0.5,0.5,0.5)
            #Taille de police et couleur

            for i in range(0, daysDisplayed):
                #Affichage de la date en haut de chaque colonne correspondant à un jour
                context.move_to((1/(4*daysDisplayed))+i*(1/daysDisplayed), 1/(2*hoursDisplayed))
                context.show_text("{:02d}/{:02d}".format((timedelta(i)+startDay).day, (timedelta(i)+startDay).month))

            for i in range(1, daysDisplayed):
                #Traçage des lignes verticales séparant les jours
                context.move_to(i/(daysDisplayed), 0)
                context.line_to(i/(daysDisplayed), 1)

            
        size = (drawingArea.get_allocation().width, drawingArea.get_allocation().height)
        context.scale(size[0], size[1])
        #Mise à l'échelle du contexte
        
        context.select_font_face("Purisa")
        #Choix de la police d'écriture
        
        drawTimeLines()
        context.set_line_width(0.002)
        context.stroke()
        #Traçage des lignes correspondant aux heures
        
        drawDayLines()
        context.set_line_width(0.001)
        context.stroke()
        #Traçage des lignes correspondant aux jours
