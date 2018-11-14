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
    def __init__(self, address=DIRECTION_ADDRESS):
        '''
        TODO: Build a gyro calibration fuction
        '''
        self.i2c     = SMBus(1)
        self.address = address
        #self.i2c.write_byte_data(self.address, DIRECTION_REG_POWER1, 
        #                         DIRECTION_SLEEP)
        self.i2c.write_byte_data(self.address, DIRECTION_REG_POWER1, 0)



    def _read_i2c_word(self, register):
        """Read two i2c registers and combine them.
        register -- the first register to read from.
        Returns the combined read results.
        """
        # Read the data from the registers
        high = self.i2c.read_byte_data(self.address, register)
        low  = self.i2c.read_byte_data(self.address, register + 1)

        value = (high << 8) + low

        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value

    def getDirection(self):
        '''
        Get sensor brigthness and return true if daylight is detected
        '''
        # wake up
        # self.i2c.write_byte_data(self.address, DIRECTION_REG_POWER1, 0)

        # measure
        x = self._read_i2c_word(DIRECTION_REG_GYROX)
        y = self._read_i2c_word(DIRECTION_REG_GYROY)
        z = self._read_i2c_word(DIRECTION_REG_GYROZ)

        Logger.debug("Direction=" + str(x/131) + "," + str(y/131) + "," + str(z/131))

        # sleep
        # self.i2c.write_byte_data(self.address, DIRECTION_REG_POWER1, 
        #                        DIRECTION_SLEEP)

        return Directions.PORTRAIT 
