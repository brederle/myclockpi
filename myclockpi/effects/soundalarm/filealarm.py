from myclockpi.engine.ialarmeffect import IAlarmEffect 
from myclockpi.effects.soundalarm.audio_ffpystream import StreamFFPy

from kivy.core.audio import SoundLoader 

class FileAlarm(IAlarmEffect):

    def __init__(self, filename):
        self.sound = SoundLoader.load(self.filename)
        if (self.sound == None):
            defaultSound = 
                os.path.join(os.path.dirname(__file__),
                "clock-chimes-daniel_simon.wav")
            self.sound = SoundLoader.load(defaultSound)
        super().__init__()

    def on_alarm(self, context):
        self.sound = SoundLoader.load(self._streamUrl)
        context.soundActor.standby(False)
        self.sound.play()
        

    def stop(self, context):
        # setting amplifier to standby makes stopping feel more smooth
        context.soundActor.standby(True)
        if (self.sound != None):
            self.sound.stop()
        
