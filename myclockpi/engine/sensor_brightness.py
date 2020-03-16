import RPi.GPIO as GPIO

class SensorBrightness:
    '''
    Class for handling the brightness sensor
    '''
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN)
        self.state            = False
        self._numLights       = 0
        self._numMeasurements = 0

    def isDayLight(self):
        '''
        Get sensor brigthness and return true if daylight is detected
        Due to sensor bias, the light detection is filtered.
        Light is detected if more tha 2/3 of 12 measurements are light
        '''
        if GPIO.input(4) == 0:
            self._numLights += 1

        self._numMeasurements += 1
        if self._numMeasurements == 8:
            self.state = True if self._numLights > 5 else False
            self._numMeasurements = 0
            self._numLights       = 0               

        return self.state

