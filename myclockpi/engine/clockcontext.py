from myclockpi.engine.sensor_brightness import SensorBrightness
from myclockpi.engine.sensor_direction import SensorDirection
from myclockpi.engine.actor_sound import ActorSound
from myclockpi.settings.repository import ClockSettingsJsonRepo

from kivy.uix.settings import SettingsWithSpinner


class ClockContext:

    def __init__(self):
        self.soundActor = ActorSound()
        self.brightnessSensor = SensorBrightness()
        #self.directionSensor  = SensorDirection()
        self.settingsPanel = SettingsWithSpinner()
        self.settingsPanel.add_kivy_panel()
