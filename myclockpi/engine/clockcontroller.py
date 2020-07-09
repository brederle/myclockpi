import os

from datetime import datetime
from kivy import kivy_home_dir
from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen

from myclockpi.engine.clockcontext import ClockContext
from myclockpi.engine.alarm_manager import AlarmManager
from myclockpi.engine.sensor_direction import SensorDirection

from myclockpi.settings.data import ClockSettings
from myclockpi.settings.repository import ClockSettingsJsonRepo


# TODO: register clockfaces automatically
from myclockpi.faces.simpledigital.simpledigiclock import SimpleDigiClock

from myclockpi.effects.soundalarm.streamalarm import StreamAlarm

modulepath = os.path.dirname(os.path.abspath(__file__))
Builder.load_file(modulepath + "/defaultstyle.kv")


class ClockControllerApp(App):
    '''
    Main class to control the clock face, alarms and all the possible settings.
    '''

    def __init__(self):
        self.context = ClockContext()
        self._screenManager = ScreenManager(transition=SlideTransition())

        Logger.info("Reading clock config: " +
                       kivy_home_dir + "/myclockpi.json")
        self.settings = ClockSettingsJsonRepo.load(
                       kivy_home_dir + "/myclockpi.json" )
        #self.testalarm = StreamAlarm("http://www.rockantenne.de/webradio/channels/soft-rock.m3u")
        #self.testalarm = StreamAlarm(
        #    "http://mp3channels.webradio.rockantenne.de/soft-rock.aac")
        #self.testalarm = StreamAlarm("http://mp3channels.webradio.rockantenne.de/rockantenne.aac")
        #self.testalarm = StreamAlarm("/home/ticktack/music/Heaven_s Basement - The Long Goodbye.mp3")
        self.brightness = None
        self.direction = None
        self.currentEffect = None
        super().__init__()

    def on_settings(self, instance):
        '''
        Open settings
        '''
        self.root.current = "settings"

    def on_stop(self, instance):
        '''
        Stop alarm
        '''
        pass

    def on_mic(self, instance):
        '''
        Microfon Mute/Unmute toggle
        '''
        pass

    def on_sleep(self, instance):
        '''
        Sleep modus enabled
        '''
        pass

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
        # if (self.direction != newDirection):
        #    self.changeDirection(newDirection)
        #self.direction = newDirection

        if (self.currentTime.second != newDateTime.second):
            # update on_time every second
            self.changeTime(newDateTime)

        if (self.currentTime.minute != newDateTime.minute):
            # check for alarm only every minute
            if AlarmManager.is_alarm_now(newDateTime):
                # start Alarm effect, do callback
                effect = filter(
                    lambda e: e.name == AlarmManager.alarm_config.effect,
                    self.settings.effects)
                EffectType = type(effect.effect_type, (), {})
                self.currentEffect = Effect(effects.links[0])
                self.currentEffect.on_alarm(self.context)
            if AlarmManager.alarm_time < newDateTime:
                # compute new alarm if old one is in the past 
                AlarmManager.next_alarm(self.settings.alarms, newDateTime)

        if (self.currentTime.day != newDateTime.day):
            # notify on date changes
            self.changeDate(newDateTime)
        self.currentTime = newDateTime

    def build(self):
        self._screenManager = ScreenManager(transition=SlideTransition())

        # main screen has to be added first to screenmanager
        self.clockFace = SimpleDigiClock()
        self.clockFace.register_actions(self.on_settings, self.on_sleep,
                                        self.on_stop, self.on_mic)

        clockFaceScreen = Screen(name="clockface")
        clockFaceScreen.add_widget(self.clockFace.currentLayout)
        self._screenManager.add_widget(clockFaceScreen)

        # this is the first "satelite" screen
        settingsScreen = Screen(name="settings")
        # settingsScreen.add_widget(ClockSettings())
        self._screenManager.add_widget(settingsScreen)
        # TODO: some default sizes; make configurable?
        self.font_size = 36

        # initialize clock scheduling
        self.currentTime = datetime.now()
        AlarmManager.next_alarm(self.settings.alarms, self.currentTime)
        self.changeTime(self.currentTime)
        self.changeDate(self.currentTime)
        Clock.schedule_interval(self.updateClockFace, 0.2)
        # self.testalarm.on_alarm(self.context)
        
        return self._screenManager
