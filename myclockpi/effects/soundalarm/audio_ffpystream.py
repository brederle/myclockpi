try:
    import ffpyplayer
    from ffpyplayer.player import MediaPlayer
    from ffpyplayer.tools import set_log_callback, get_log_callback, formats_in
except:
    raise

from kivy.core.audio.audio_ffpyplayer import SoundFFPy

class StreamFFPy(SoundFFPy):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load(self):
        self.unload()
        ff_opts = {'vn': True, 'sn': True}  # only audio
        self._ffplayer = MediaPlayer(self.source,
                                     callback=self._player_callback,
                                     loglevel='info', ff_opts=ff_opts)
        player = self._ffplayer
        player.set_volume(self.volume)
        player.toggle_pause()
        self._state = 'paused'
