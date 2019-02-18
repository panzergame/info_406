import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class DateTimeDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Date & Time", parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.time_box = TimeBox()

        self.set_default_size(200, 200)
        self.calendar = Gtk.Calendar()
        main_box = self.get_content_area()
        main_box.add(self.calendar)
        main_box.add(self.time_box)
        self.show_all()


    @property
    def hour(self):
        return self.time_box.spin_hour.get_value_as_int()

    @property
    def minute(self):
        return self.time_box.spin_minute.get_value_as_int()

    @property
    def year(self):
        year , month , day = self.calendar.get_date()
        return year

    @property
    def month(self):
        year , month , day = self.calendar.get_date()
        return month

    @property
    def day(self):
        year , month , day = self.calendar.get_date()
        return day



class TimeBox(Gtk.Box):

    def __init__(self):
        Gtk.Box.__init__(self ,spacing = 10)
        self.set_border_width(10)

        label = Gtk.Label(" h ")

        adjustment_hour = Gtk.Adjustment(0,0, 23, 1, 10, 0)
        self.spin_hour = Gtk.SpinButton()
        self.spin_hour.set_adjustment(adjustment_hour)

        adjustment_minute = Gtk.Adjustment(0,0, 59, 1 , 10, 0)
        self.spin_minute = Gtk.SpinButton()
        self.spin_minute.set_adjustment(adjustment_minute)

        self.add(self.spin_hour)
        self.add(label)
        self.add(self.spin_minute)
