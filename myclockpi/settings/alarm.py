import 

class AlarmConfig:

    def __init__(self, name="",
            time = ,
            days= [],
            effect = "",
            enabled = true):
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
        self.time = time
        self.days = days if isinstance(days, list) else [ days ]
        self.effect = effect
        self.nabled = enabled

 
