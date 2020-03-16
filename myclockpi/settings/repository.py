import json
import datetime

from myclockpi.settings.data import ClockSettings, AlarmConfig, EffectConfig

class ClockSettingsJsonRepo:

    @staticmethod
    def _as_settings(values):
        if 'face' in values:
            # this mandatory element marks top-level structure
            settings = ClockSettings(face=values['face']) 
            if 'alarms' in values:
                for alarm in values['alarms']:
                    settings.alarms.append(AlarmConfig(**alarm))
            if 'effects' in values:
                for effect in values['effects']:
                    settings.effects.append(EffectConfig(**effect))
            return settings
        else:
            return values

    @classmethod    
    def load(cls, path, default={}):
        '''Load myclockpi json file given the filepath
           :param path  file path to json
           :param default default setting to use if no file is found'''
        try:
            with open(path, 'r') as jsonfile:
                cls.settings = json.load(jsonfile,
                        object_hook=cls._as_settings)
        except FileNotFoundError:
            cls.settings = default
        return cls.settings

    class ObjectEncoder(json.JSONEncoder):
        TIME_FORMAT = "%H:%M"
        def default(self, obj):
            if isinstance(obj, datetime.time):
                return obj.strftime(self.TIME_FORMAT)
            elif isinstance(obj, object):
                return vars(obj)
            else:
                # Let the base class default method raise the TypeError
                return json.JSONEncoder.default(self, obj)

    @classmethod
    def store(cls, settings, path):
        with open(path, 'w') as jsonfile:
            json.dump(settings.__dict__, jsonfile,
                cls=cls.ObjectEncoder, indent=2)
