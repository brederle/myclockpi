from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

#Builder.load_file("./simpledigiclock.kv")

class SimpleDigiClock(BoxLayout):
    clockValue   = ObjectProperty(None)
    dateValue    = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(BoxLayout,self).__init__(**kwargs)
        Logger.info(self.clockValue)
        self.clockFormat  = self.clockValue.text 
        self.dateFormat   = self.dateValue.text

    def setTime(self, newTime):
        tm = newTime.strftime(self.clockFormat)
        self.clockValue.text = tm

    def setDate(self, newTime):
        tm = newTime.strftime(self.dateFormat)
        self.dateValue.text = tm

class SimpleDigiClockApp(App):
    
    def updateClock(self, delta):
        newDateTime = datetime.now()

        if (self.currentTime.second != newDateTime.second):
            self.clockFace.setTime(newDateTime)

        if (self.currentTime.day != newDateTime.day):
           self.clockface.setDate(newDateTime)

        self.currentTime = newDateTime


    def build(self):
        self.currentTime = datetime.now()
        self.clockFace = SimpleDigiClock()
        self.clockFace.setTime(self.currentTime)
        self.clockFace.setDate(self.currentTime)
        Clock.schedule_interval(self.updateClock, 0.2)
        return self.clockFace

if __name__ == '__main__':
    SimpleDigiClockApp().run()
