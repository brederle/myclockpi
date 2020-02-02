from kivy.logger import Logger
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty

from kivy.uix.settings import SettingsWithSpinner

class ClockSettings(SettingsWithSpinner):

    __events__ = ('on_close', )

    def __init__(self, **kwargs):
        # this is the fist "satelite" screen
        super().__init__(**kwargs)
        self.add_kivy_panel()
   
    def on_close(self, *args):
       app = App.get_running_app()
       app.root.current = "clockface" 
