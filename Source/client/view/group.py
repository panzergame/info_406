import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Source.client.model.common import *


class Group(Gtk.Box):

    def __init__(self, common):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.title = Gtk.Label("\tGroupes : ", xalign=0)
        #self.groupList = self.put_groups(common.user_clicked)
        self.add(self.title)
        #self.add(self.groupList)
        self.test(common.user_clicked)

    def test(self, user):
        groupList = self.put_groups(user)
        self.add(groupList)

    def put_groups(self, user):
        groupList = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        groups = user.groups
        for group in groups:
            groupLine = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            color = Gtk.ColorButton()
            name = Gtk.Label(group.name, xalign=0)
            agendasList = self.put_agendas(group)
            groupLine.pack_start(color, False, True, 0)
            groupLine.pack_start(name, False, True, 0)
            groupLine.pack_start(agendasList, False, True, 0)
            groupList.add(groupLine)
        return groupList

    def put_agendas(self, group):
        agendasList = Gtk.ListBox()
        agendas = group.agendas
        for agenda in agendas:
            name = Gtk.Label(agenda.name, xalign=0)
            agendasList.add(name)
        return agendasList
