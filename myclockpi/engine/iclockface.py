from abc import ABC, abstractmethod

from myclockpi.clockcontext import ClockContext


class IClockFace(ABC):
    '''
    Define the interface for clock faces.
    '''
    @abstractmethod
    def register_actions(self, on_settings, on_sleep, on_stop, on_mic ):
        '''
        Register callback that can and should be handled by clockcontroller.
        '''
        pass

    @abstractmethod
    def on_brightness(self, context, isLight):
        '''
        Change clock face depending on value of brightness sensor 
                        
        :param ClockContext context: the context with all accessible sensors/actors
        :param Boolean isLight: true is daylight is detected, False if dark
        '''
        pass

    @abstractmethod
    def on_direction(self, context, direction):
        '''
        Change clock face depending on value of direction sensor 
    
        :param ClockContext context: the context with all accessible sensors/actors
        :param Directions direction: one of the main clock display directions
        '''
        pass

    @abstractmethod    
    def on_time(self, context, newTime):
        '''
        Show the new time, every second.
        :param ClockContext context: the context with all accessible sensors/actors
        :param datetime newTime: the new datetime value
        '''
        pass

    @abstractmethod
    def on_date(self, context, newTime):
        '''
        Show the new date, every day.

        :param ClockContext context: the context with all accessible sensors/actors
        :param datetime newTime: the new datetime value
        '''
        pass
