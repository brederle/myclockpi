from datetime import datetime
from kivy.app import App
from kivy.clock import Clock

import RPi.GPIO as GPIO

from simpledigiclock.simpledigiclock import SimpleDigiClock
from myclockpi.sensor_brightness import SensorBrightness
from myclockpi.sensor_direction import SensorDirection



class ClockControllerApp(App):
    '''
    Main class to control the clock face, alarms and all the possible settings.
    '''

    def changeBrightness(self, isLight):
        '''
        Change clock face depending on value of brightness sensor 
    
        :param Boolean isLight: true is daylight is detected, False if dark
        '''
        self.clockFace.on_brightness(isLight) 

    def changeDirection(self, direction):
        '''
        Change clock face depending on value of direction sensor 
    
        :param Directions direction: one of the main clock display directions
        '''
        self.clockFace.on_direction(direction) 

    def _initAmplifier(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT, initial=0)
        GPIO.output(18, GPIO.LOW)

    def updateClockFace(self, delta):
        newDateTime = datetime.now()

        newBrightness = brightnessSensor.isDayLight()
        if (self.brightness != newBrightness):
            changeBrightness(newBrightness)
        self.brightness = newBrightness

        newDirection = directionSensor.getDirection()
        if (self.direction != newDriection):
            changeDirection(newDirection)
        self.direction = newDirection

        if (self.currentTime.second != newDateTime.second):
            self.clockFace.changeTime(newDateTime)
        if (self.currentTime.day != newDateTime.day):
           self.clockface.changeDate(newDateTime)
        self.currentTime = newDateTime



    def build(self):
        self._initAmplifier()
        
        self.brightnessSensor = SensorBrightness()
        self.brightness = None

        self.directionSensor = SensorDirection()
        self.direction = None

        self.currentTime = datetime.now()
        self.clockFace = SimpleDigiClock()
        self.clockFace.setTime(self.currentTime)
        self.clockFace.setDate(self.currentTime)
        Clock.schedule_interval(self.updateClockFace, 0.2)
        return self.clockFace
