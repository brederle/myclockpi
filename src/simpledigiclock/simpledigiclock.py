from datetime import datetime
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from myclockpi.iclockface import IClockFace


class SimpleDigiClockLayout(BoxLayout):
    clockValue   = ObjectProperty(None)
    dateValue    = ObjectProperty(None)

    def __init__(self, filename, **kwargs):
        Builder.load_file("./simpledigiclock/" + filename)
        super(BoxLayout,self).__init__(**kwargs)
        Logger.debug("Clock digit format: ", self.clockValue)
        self.clockFormat  = self.clockValue.text 
        self.dateFormat   = self.dateValue.text

class SimpleDigiClock(IClockFace):

    def __init__(self):
        '''
        Init simpledigiclock with a portrait and a landscape layout
        '''
        portraitLayout  = SimpleDigiClockLayout(
            filename="simpledigiclock_p.kv") 
        landscapeLayout = SimpleDigiClockLayout(
            filename="simpledigiclock_l.kv") 
        currentLayout   = landscapeLayout


    def on_brightness(self, isLight):
        Logger.info("Brightness: " + isLight)

    def on_direction(self, direction):
        Logger.info("Direction: " + direction)

    def on_time(self, newTime):
        '''
        Output new time with layout taken from the field content in the
        current layout
        '''
        tm = newTime.strftime(currentLayout.clockFormat)
        currentLayout.clockValue.text = tm

    def on_date(self, newTime):
        '''
        Output new date with layout taken from the field content in the
        current layout
        '''
        tm = newTime.strftime(currentLayout.dateFormat)
        currentLayout.dateValue.text = tm

