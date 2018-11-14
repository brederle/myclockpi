from datetime import datetime
from kivy.app import App
from kivy.clock import Clock

from myclockpi.clockcontext import ClockContext
from myclockpi.sensor_brightness import SensorBrightness
from myclockpi.sensor_direction import SensorDirection

# TODO: register clockfaces automatically
from simpledigiclock.simpledigiclock import SimpleDigiClock

from streamalarm.streamalarm import StreamAlarm

class ClockControllerApp(App):
    '''
    Main class to control the clock face, alarms and all the possible settings.
    '''

    def __init__(self):
        self.context = ClockContext()        
        #self.testalarm = StreamAlarm("http://www.rockantenne.de/webradio/channels/soft-rock.m3u")
        self.testalarm = StreamAlarm("http://mp3channels.webradio.rockantenne.de/rockantenne.aac")
        #self.testalarm = StreamAlarm("/home/ticktack/music/Heaven_s Basement - The Long Goodbye.mp3")
        self.brightness = None
        self.direction  = None
        super().__init__()

    def changeBrightness(self, isLight):
        '''
        Change clock face depending on value of brightness sensor 
    
        :param Boolean isLight: true is daylight is detected, False if dark
        '''
        self.clockFace.on_brightness(self.context, isLight) 

    def changeDirection(self, direction):
        '''
        Change clock face depending on value of direction sensor 
    
        :param Directions direction: one of the main clock display directions
        '''
        self.clockFace.on_direction(self.context, direction) 

    def changeDate(self, date):
        '''
        Change clock face depending on value of direction sensor 
    
        :param Directions direction: one of the main clock display directions
        '''
        self.clockFace.on_date(self.context, date)

    def changeTime(self, time):
        '''
        Change clock face depending on value of direction sensor 
    
        :param Directions direction: one of the main clock display directions
        '''
        self.clockFace.on_time(self.context, time)


    def updateClockFace(self, delta):
        newDateTime = datetime.now()

        newBrightness = self.context.brightnessSensor.isDayLight()
        if (self.brightness != newBrightness):
            self.changeBrightness(newBrightness)
        self.brightness = newBrightness

        #newDirection = self.context.directionSensor.getDirection()
        #if (self.direction != newDirection):
        #    self.changeDirection(newDirection)
        #self.direction = newDirection

        if (self.currentTime.second != newDateTime.second):
           self.changeTime(newDateTime)
        if (self.currentTime.day != newDateTime.day):
           self.changeDate(newDateTime)
        self.currentTime = newDateTime


    def build(self):
        self.currentTime = datetime.now()
        self.clockFace = SimpleDigiClock()
        self.changeTime(self.currentTime)
        self.changeDate(self.currentTime)
        Clock.schedule_interval(self.updateClockFace, 0.2)
        self.testalarm.on_alarm(self.context)
        return self.clockFace.currentLayout
