import json

from myclockpi.settings.clock import ClockConfig
from myclockpi.settings.alarm import AlarmConfig
from myclockpi.settings.effect import AlarmEffectConfig


class ClockSettings:
    def __init__(self):
       self.clock  = ClockConfig()
       self.alarms = []
       self.skins = []
       self.effects = []

class ClockSettingsJsonRepo

    @staticmethod
    def _as_settings(values):
       	if 'alarms' in values:
            # FIXME: use face as marking label later
            settings = ClockSettings()          
            settings.clock = ClockConfig(
            face = values['face'])
            for alarm in values['alarms']:
                settings.alarms.add(AlarmConfig(
                   name = alarm['name'],
                   time = alarm['time'],
                   days = alarm['days'],
                   alarm_type = alarm['type'],
                   effect = alarm['effect'],
                   enabled = bool(alarm['enabled']))
            for effect in values['effects']:
                settings.effects.add(AlarmEffectConfig(
                    name = effect['name'],
                    effect_type = effect['type'],
                    links = effect['links']
                ))
            return settings
        else:
            return values


    def __init__(self, path):
	self.jsonPath = path
        self.settings = ClockSettings()          

    def load(self):
        with open(self.path, 'r') as jsonfile:
            cls.settings = json.load(jsonfile, )                
        return cls.settings

    def store(self, settings=None, path=""):
        if not settings:
            settings = self.settings
        else:
            self.settings = settings

        with open(path, 'w') as jsonfile:
            json.dump(self..settings, jsonfile)
        
