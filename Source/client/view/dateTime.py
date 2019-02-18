import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class DateTimeBox(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Date & Time", parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(200, 200)
        calendar = Gtk.Calendar()
        main_box = self.get_content_area()
        main_box.add(calendar)
        main_box.add(TimeBox())
        self.show_all()


class TimeBox(Gtk.Box):

    def __init__(self):
        Gtk.Box.__init__(self ,spacing = 10)
        self.set_border_width(10)

        label = Gtk.Label(" h ")

        adjustment_hour = Gtk.Adjustment(0,0, 23, 1, 10, 0)
        hour = Gtk.SpinButton()
        hour.set_adjustment(adjustment_hour)

        adjustment_minute = Gtk.Adjustment(0,0, 59, 1 , 10, 0)
        minute = Gtk.SpinButton()
        minute.set_adjustment(adjustment_minute)

        self.add(hour)
        self.add(label)
        self.add(minute)
