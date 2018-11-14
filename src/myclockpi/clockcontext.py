from myclockpi.sensor_brightness import SensorBrightness
from myclockpi.sensor_direction import SensorDirection
from myclockpi.actor_sound import ActorSound

class ClockContext:

    def __init__(self):
        self.soundActor       = ActorSound()
        self.brightnessSensor = SensorBrightness()
        #self.directionSensor  = SensorDirection()


