from myclockpi.ialarmeffect import IAlarmEffect 
from soundalarm.audio_ffpystream import StreamFFPy

from kivy.core.audio import SoundLoader 

class StreamAlarm(IAlarmEffect):

    def __init__(self, streamUrl):
        self.sound = StreamFFPy()
        self.sound.source = streamUrl
        super().__init__()

    def on_alarm(self, context):
        #self.sound = SoundLoader.load(self._streamUrl)
        self.sound.load()
        context.soundActor.standby(False)
        if (self.sound != None):
            self.sound.play()

    def stop(self, context):
        # setting amplifier to standby makes stopping feel more smooth
        context.soundActor.standby(True)
        if (self.sound != None):
            self.sound.stop()
        
