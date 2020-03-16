from abc import ABC, abstractmethod

from myclockpi.engine.clockcontext import ClockContext


class IAlarmEffect(ABC):
    '''
    Define the interface for alarm effects.
    '''

    @abstractmethod
    def on_alarm(self, context):
        '''
        Initiate effect on alarm                
        :param ClockContext context: the context with all accessible sensors/actors
        '''
        pass

    @abstractmethod
    def stop(self, context):
        '''
        Stop effect
        '''
        pass
