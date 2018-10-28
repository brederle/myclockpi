from smbus2 import SMBus
from kivy.logger import Logger

from enum import Enum

class Directions(Enum):
    LANDSCAPE            = 1
    LANDSCAPE_UPSIDEDOWN = 2
    PORTRAIT             = 3
    PORTRAIT_UPSIDEDOWN  = 4
    FACEDOWN             = 5
    BACKWARD             = 6

DIRECTION_ADDRESS    = 0x68
DIRECTION_REG_POWER1 = 0x6b
DIRECTION_SLEEP      = 0x40

DIRECTION_REG_GYROX  = 0x43
DIRECTION_REG_GYROY  = 0x45
DIRECTION_REG_GYROZ  = 0x47

class SensorDirection:
    '''
    Class for handling the gyro and detecting display direction
    '''
    def __init__(self):
        '''
        TODO: Build a gyro calibration fuction
        '''
        i2c = SMBus(1)
        i2c.write_byte_data(DIRECTION_ADDRESS, DIRECTION_REG_POWER1, 
                            DIRECTION_SLEEP)

    def getDirection(self):
        '''
        Get sensor brigthness and return true if daylight is detected
        '''
        # wake up
        i2c.write_byte_data(DIRECTION_ADDRESS, DIRECTION_REG_POWER1, 0)

        # measure
        x = i2c.read_word_data(DIRECTION_ADDRESS, DIRECTION_REG_GYROX)
        y = i2c.read_word_data(DIRECTION_ADDRESS, DIRECTION_REG_GYROY)
        z = i2c.read_word_data(DIRECTION_ADDRESS, DIRECTION_REG_GYROZ)

        Logger.debug("Direction=" + x + "," + y + "," + z)

        # sleep
        i2c.write_byte_data(DIRECTION_ADDRESS, DIRECTION_REG_POWER1, 
                            DIRECTION_SLEEP)

        return Directions.PORTRAIT 
