from abc import ABC, abstractmethod

class IClockFace(ABC):
    '''
    Define the interface for clock faces.
    '''

    @abstractmethod
    def on_brightness(self, isLight):
        '''
        Change clock face depending on value of brightness sensor 
                        
        :param Boolean isLight: true is daylight is detected, False if dark
        '''
        pass

    @abstractmethod
    def on_direction(self, direction):
        '''
        Change clock face depending on value of direction sensor 
    
        :param Directions direction: one of the main clock display directions
        '''
        pass

    @abstractmethod    
    def on_time(self, newTime):
        '''
        Show the new time, every second.
    
        :param datetime newTime: the new datetime value
        '''
        pass

    @abstractmethod
    def on_date(self, newTime):
        '''
        Show the new date, every day.

        :param datetime newTime: the new datetime value
        '''
        pass
