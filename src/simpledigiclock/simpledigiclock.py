from datetime import datetime
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty

from myclockpi.iclockface import IClockFace

class SimpleDigiClockLayout(BoxLayout):
    clockValue  = ObjectProperty(None)
    dateValue   = ObjectProperty(None)
    clockColor  = ListProperty(None)
    frontColor  = ListProperty(None)
    # alarmState  = StringProperty(None) 

    def __init__(self):
        super().__init__()
        #Logger.debug("Clock digit format: ", self.clockValue.text)
        self.clockFormat = self.clockValue.text 
        self.dateFormat  = self.dateValue.text


Builder.load_file("./simpledigiclock/simpledigiclock_l.kv")

class SimpleDigiClockLandscape(SimpleDigiClockLayout):

    def __init__(self):
        super().__init__()



Builder.load_file("./simpledigiclock/simpledigiclock_p.kv")

class SimpleDigiClockPortrait(SimpleDigiClockLayout):

    def __init__(self):
        super().__init__()


class SimpleDigiClock(IClockFace):
    def __init__(self):
        '''
        Init simpledigiclock with a portrait and a landscape layout
        '''
        super().__init__()
        self.portraitLayout  = SimpleDigiClockPortrait() 
        self.landscapeLayout = SimpleDigiClockLandscape()
        self.currentLayout   = self.landscapeLayout


    def on_brightness(self, context, isLight):
        Logger.info("Brightness: " + str(isLight))
        if isLight:
            self.currentLayout.clockColor[3] = 1.0
            self.currentLayout.frontColor[3] = 1.0
        else:
            self.currentLayout.clockColor[3] = 0.3
            self.currentLayout.frontColor[3] = 0.2 

    def on_direction(self, context, direction):
        Logger.info("Direction: " + str(direction))

    def on_time(self, context, newTime):
        '''
        Output new time with layout taken from the field content in the
        current layout
        '''
        tm = newTime.strftime(self.currentLayout.clockFormat)
        self.currentLayout.clockValue.text = tm

    def on_date(self, context, newTime):
        '''
        Output new date with layout taken from the field content in the
        current layout
        '''
        tm = newTime.strftime(self.currentLayout.dateFormat)
        self.currentLayout.dateValue.text = tm

