from myclockpi.sensor_brightness import SensorBrightness
from myclockpi.sensor_direction import SensorDirection
from myclockpi.actor_sound import ActorSound
from myclockpi.settings.repository import ClockSettingsJsonRepo

from kivy.uix.settings import SettingsWithSpinner

class ClockContext:

    def __init__(self):
        self.soundActor       = ActorSound()
        self.brightnessSensor = SensorBrightness()
        #self.directionSensor  = SensorDirection()
        self.settingsPanel    = SettingsWithSpinner() 
        self.settingsPanel.add_kivy_panel()

