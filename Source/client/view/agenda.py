import cairo
from datetime import *
import random

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AgendaBox(Gtk.Box):
    def __init__(self, agenda, day):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        overlay = Gtk.Overlay()
        overlay.add(AgendaTimeAnnotations(day)) 
        overlay.add_overlay(AgendaEvents(agenda.all_events, day))
        self.add(overlay)


class AgendaEvents(Gtk.DrawingArea):
    
    def __init__(self, events, day):
        
        def draw(da, ctx):
            AgendaEvents.drawAllEvents(da, ctx, events, day)
            
        Gtk.DrawingArea.__init__(self)
        self.set_property("expand",True)
       
        self.connect('draw', draw)

    def drawAllEvents(drawingArea, context, events, firstDay):
        size = (drawingArea.get_allocation().width, drawingArea.get_allocation().height)
        context.scale(size[0], size[1]) 
        for event in events:
            color = ((event.start.hour/24),(event.start.day/30),(event.start.month/12))
            #todo mettre une vraie sélection de couleur
            
            context.set_font_size((1/2)*(1/24))
            #Moitié de l'espace représenté pour une heure
            
            AgendaEvents.drawEvent(drawingArea, context, event, firstDay, color)
            context.fill()

        
    def drawEvent(drawingArea, context, event, firstDay, color):
        minutesPerDay = 24*60
        daysDisplayed = 7
        
        def toDayMinutes(date):
            if type(date) == datetime:
                return date.minute + date.hour*60
            elif type(date) == timedelta:
                #Temps en secondes
                return (date.seconds/60)
            else:
                raise ValueError
        
        
        def getSlotCoords(start, end, firstDay):
            
            x = (start-firstDay).days*(1/daysDisplayed)
            y = (toDayMinutes(start)/(minutesPerDay))
            width = (1/daysDisplayed)
            height = (toDayMinutes(end - start)/(minutesPerDay))

            return x, y, width, height

        def drawEventInfo(drawingArea, context, event):
            color = context.get_source_rgb()
            
        context.set_source_rgb(color[0],color[1],color[2])
        
        x, y, width, height = getSlotCoords(event.start, event.end, firstDay)
        context.rectangle(x, y, width, height)
        context.fill()

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
        
        context.move_to(x_text,y_text+1/48)#Décalage de 1/2 heure
        context.show_text("{:02d}h{:02d}-{:02d}h{:02d}".format(event.start.hour, event.start.minute, event.end.hour, event.end.minute))
        
        



class AgendaTimeAnnotations(Gtk.DrawingArea):   
    def __init__(self, startDay):
        day  = startDay
        def draw(da, ctx):
            AgendaTimeAnnotations.drawAnnotations(da, ctx, day)
            
        Gtk.DrawingArea.__init__(self)
        self.set_property("expand",True)
        self.connect('draw', draw)

    def drawAnnotations(drawingArea, context, startDay):
        daysDisplayed = 7
        hoursDisplayed = 24
        def drawTimeLines():
            dashes=[(1/70),(1/70)]
            context.set_dash(dashes)
            context.set_font_size((1/3)*(1/hoursDisplayed))
            context.set_source_rgb(0.5, 0.5, 0.5)
            
            for i in range(1, hoursDisplayed):
                context.move_to(0.002, (i/hoursDisplayed)-0.002)
                context.show_text("{}h".format(i))
                
                context.move_to(0, i/hoursDisplayed)
                context.line_to(1, i/hoursDisplayed)

        def drawDayLines():
            dashes=[1,0]
            context.set_dash(dashes)
            context.set_font_size(((1/2)*(1/hoursDisplayed)))
            context.set_source_rgb(0.5,0.5,0.5)

            for i in range(0, daysDisplayed):
                context.move_to((1/(4*daysDisplayed))+i*(1/daysDisplayed), 1/(2*hoursDisplayed))
                context.show_text("{:02d}/{:02d}".format((timedelta(i)+startDay).day, (timedelta(i)+startDay).month))

            for i in range(1, daysDisplayed):    
                context.move_to(i/(daysDisplayed), 0)
                context.line_to(i/(daysDisplayed), 1)

            
        size = (drawingArea.get_allocation().width, drawingArea.get_allocation().height)
        context.scale(size[0], size[1])
        context.select_font_face("Purisa")
             
        
        drawTimeLines()
        context.set_line_width(0.002)
        context.stroke()
        drawDayLines()
        context.set_line_width(0.001)
        context.stroke()
        

############CLASSES TEMPO ##################################
class tempAgenda():
    def __init__(self, events):
        self.all_events = events

class tempEvent():
    def __init__(self):
        #todo supprimer
        self.type="Manger"
        self.start=datetime(2019,1,2,8,0)
        self.end=datetime(2019,1,2,23,30)

class tempEvent2():
    def __init__(self):
        #todo supprimer
        self.type="Dormir"
        self.start=datetime(2019,1,3,12,0)
        self.end=datetime(2019,1,3,20,0)

class tempEvent3():
    def __init__(self):
        #todo supprimer
        self.type="Mourir"
        self.start=datetime(2019,1,6,6,0)
        self.end=datetime(2019,1,6,10,15)

################################# TESTS  ###########################################

agenda = tempAgenda([tempEvent(), tempEvent2(),tempEvent3()])

class MyWindow(Gtk.Window):
    def __init__(self):
            
        Gtk.Window.__init__(self, title="Hello World")
        self.add(AgendaBox(agenda, datetime(2019,1,1)))
        
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
