import datetime
import unittest
import os

from myclockpi.settings.repository import ClockSettingsJsonRepo
from myclockpi.settings.data import ( ClockSettings, AlarmConfig, EffectConfig )


class TestClockSettingsJsonRepo(unittest.TestCase):


    def setUp(self):
        self.jsonFilename = "/tmp/myclockpi_testconfig.json" 

        self.testConfig = ClockSettings(
            face="mydigital",
            alarms = [ 
                AlarmConfig(
                    waketime=datetime.time(7, 0), 
                    name="work",
                    days=[1,2,3,4,5],
                    effect="softrock",
                    enabled=False
                ),
                AlarmConfig(
                    waketime=datetime.time(20, 15), 
                    name="flight",
                    days=[],
                    effect="softrock",
                    enabled=True
                ),
            ],
            effects = [
                EffectConfig(
                    name="softrock",
                    links=['http://mp3channels.webradio.rockantenne.de/soft-rock.aac'],
                    effect_type="stream"
                ),
            ],
            skins = []
        )
        if os.path.exists(self.jsonFilename):
            os.remove(self.jsonFilename)
             

    def _cleanup_testfile(self):
        if os.path.exists(self.jsonFilename):
            os.remove(self.jsonFilename)


    def test_store_load(self):
        self.assertFalse(os.path.exists(self.jsonFilename)) 
        ClockSettingsJsonRepo.store(self.testConfig, self.jsonFilename)
        self.addCleanup(self._cleanup_testfile)        
     
        test_config1 = ClockSettingsJsonRepo.load(self.jsonFilename)
        self.assertTrue(hasattr(test_config1, 'face'))        
        self.assertTrue(hasattr(test_config1, 'alarms'))        
        self.assertTrue(hasattr(test_config1, 'effects'))        
        self.assertEqual(test_config1.face, 'mydigital')

        findalarm = list(filter(lambda x: isinstance(x, AlarmConfig) 
             and x.name=='work', test_config1.alarms))
        self.assertEqual(len(findalarm), 1)
        alarm1 = findalarm[0]
        self.assertEqual(alarm1.waketime, datetime.time(7, 0))
        self.assertEqual(alarm1.effect, "softrock")
        self.assertFalse(alarm1.enabled)
        self.assertEqual(alarm1.days, [1,2,3,4,5])

        findalarm = list(filter(lambda x: isinstance(x, AlarmConfig) 
             and x.name=='flight', test_config1.alarms))
        self.assertEqual(len(findalarm), 1)
        alarm2 = findalarm[0]
        self.assertEqual(alarm2.waketime, datetime.time(20, 15))
        self.assertEqual(alarm2.effect, "softrock")
        self.assertTrue(alarm2.enabled)
        self.assertEqual(alarm2.days, [])


    def test_default(self):
        self.assertFalse(os.path.exists(self.jsonFilename)) 
        test_config1 = ClockSettingsJsonRepo.load(self.jsonFilename,
                default={})
        self.assertEqual(test_config1, {})
        self.addCleanup(self._cleanup_testfile)        
 
if __name__ == '__main__':
    unittest.main()
