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
        overlay.add(AgendaEvents(agenda.events, day))
        overlay.add_overlay(AgendaTimeAnnotations())
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
            context.set_source_rgb((event.start.hour/24),(event.start.day/30),(event.start.month/12))
            #todo mettre une vraie sélection de couleur
            AgendaEvents.drawEvent(drawingArea, context, event, firstDay)
            context.fill()

        
    def drawEvent(drawingArea, context, event, firstDay):
        def toDayMinutes(date):
            if type(date) == datetime:
                return date.minute + date.hour*60
            elif type(date) == timedelta:
                #Temps en secondes
                return (date.seconds/60)
            else:
                #todo je ne sais pas
                raise ValueError
        
        
        def getSlotCoords(start, end, firstDay):
            minutesPerDay = 24*60
            daysDisplayed = 7
            
            x = (start-firstDay).days*(1/daysDisplayed)
            y = (toDayMinutes(start)/(minutesPerDay))
            width = (1/daysDisplayed)
            height = (toDayMinutes(end - start)/(minutesPerDay))

            return x, y, width, height


        x, y, width, height = getSlotCoords(event.start, event.end, firstDay)
        context.rectangle(x, y, width, height)


class AgendaTimeAnnotations(Gtk.DrawingArea):   
    def __init__(self):
        def draw(da, ctx):
            AgendaTimeAnnotations.drawAnnotations(da, ctx)
            
        Gtk.DrawingArea.__init__(self)
        self.set_property("expand",True)
        self.connect('draw', draw)

    def drawAnnotations(drawingArea, context):
        def drawTimeLines():
            hoursDisplayed = 24
            def initStyle():
                context.set_font_size((1/3)*(1/hoursDisplayed))
                context.set_source_rgb(0.5, 0.5, 0.5)

            initStyle()
            
            for i in range(1, hoursDisplayed):
                context.move_to(0.002, (i/hoursDisplayed)-0.002)
                context.show_text("{}h".format(i))
                
                context.move_to(0, i/hoursDisplayed)
                context.line_to(1, i/hoursDisplayed)
            
        size = (drawingArea.get_allocation().width, drawingArea.get_allocation().height)
        context.scale(size[0], size[1])
        context.select_font_face("Purisa")
        
        
        
        dashes=[(1/70),(1/70)]
        context.set_dash(dashes)
        
        drawTimeLines()
        
        context.set_line_width(0.002)
        context.stroke()

############CLASSES TEMPO ##################################
class tempAgenda():
    def __init__(self, events):
        self.events = events

class tempEvent():
    def __init__(self):
        #todo supprimer
        self.start=datetime(2019,1,2,8,0)
        self.end=datetime(2019,1,2,23,30)

class tempEvent2():
    def __init__(self):
        #todo supprimer
        self.start=datetime(2019,1,3,12,0)
        self.end=datetime(2019,1,3,20,0)

################################# TESTS  ###########################################

agenda = tempAgenda([tempEvent(), tempEvent2()])

class MyWindow(Gtk.Window):
    def __init__(self):
            
        Gtk.Window.__init__(self, title="Hello World")
        self.add(AgendaBox(agenda, datetime(2019,1,1)))
        
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
