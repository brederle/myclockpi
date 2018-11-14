import RPi.GPIO as GPIO

class ActorSound:

    def __init__(self):
        '''
        Init amplifier in standby mode
        '''
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT, initial=0)
        GPIO.output(18, GPIO.LOW)

    def standby(self, state):
       '''
       Wake up amplifier or put to sleep
       state: true if amplifier is asleep, false to activate 
       '''
       if state:
          GPIO.output(18, GPIO.LOW)
       else:
          GPIO.output(18, GPIO.HIGH)
