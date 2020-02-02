class AlarmEffectConfig:

    def __init__(self, 
        name,
        links = [],
        effect_type = "sound"):
        """Configuration for different alarm effects
        :param name: the name to refer the effect in alarms
        :param link: a list of linkd to file or internet stream or service
        :param effect_type: the type of 
        :default play a sound file 
        """
        self.name = name
        self.links = links if isinstance(links, list) else [ links ]
        self.effect_type = effect_type

