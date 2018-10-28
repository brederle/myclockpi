import RPi.GPIO as GPIO

class SensorBrightness:
    '''
    Class for handling the brightness sensor
    '''
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN)

    def isDayLight(self):
        '''
        Get sensor brigthness and return true if daylight is detected
        '''
        return True if GPIO.input(4)==0 else False 
