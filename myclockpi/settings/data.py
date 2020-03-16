import json
import datetime
import time

class AlarmConfig:
    def __init__(self,
                 waketime,
                 name="",
                 days=[],
                 effect="",
                 enabled=True):
        """Configuration for an alarm entry
        :param name  name of the alarm
        :default ""
        :param time  a time object for the alarm time
        :default "7:00 (am)"
        :param effect  name of the effect to launch for alarm
        :default "" means None, only visual alarm on skin (if supported)
        :param enabled  switch to enable/disable an alarm
        :default true means enabled
        """
        self.name = name
        if isinstance(waketime, datetime.time):
            self.waketime = waketime
        else:
            self.waketime = datetime.time(
                    *(time.strptime(waketime, "%H:%M")[3:5]))
            # FIXME for python 3.8
            # self.time = datetime.strptime(time, "%H:%M").time()
        self.days = days if isinstance(days, list) else [days]
        self.effect = effect
        self.enabled = enabled


class EffectConfig:
    def __init__(self,
                 name,
                 links=[],
                 effect_type="sound"):
        """Configuration for different alarm effects
        :param name: the name to refer the effect in alarms
        :param link: a list of linkd to file or internet stream or service
        :param effect_type: the type of
        :default play a sound file
        """
        self.name = name
        self.links = links if isinstance(links, list) else [links]
        self.effect_type = effect_type


class ClockSettings:
    def __init__(self, face="simpledigital", alarms=[], skins=[], effects=[]):
        self.face = face
        self.alarms = alarms
        self.skins = skins
        self.effects = effects
