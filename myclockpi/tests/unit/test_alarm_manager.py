import unittest
import os

from datetime import datetime

from myclockpi.engine.alarm_manager import AlarmManager
from myclockpi.settings.data import AlarmConfig


class TestAlarmManager(unittest.TestCase):

    def test_uninitialized(self):
        self.assertFalse(AlarmManager.is_alarm_now(datetime.now()))
    
    def test_enabled(self):
        timepoint = datetime(day=1, month=3, year=2020, hour=6, minute=13)

        alarm1 = AlarmConfig(waketime='7:15', days=[], enabled=False)        
        self.assertEqual(datetime.max,
            AlarmManager._alarm_time(alarm1, timepoint))

        alarm2 = AlarmConfig(waketime='7:15', days=[], enabled=True)        
        self.assertEqual(timepoint.replace(hour=7, minute=15),
            AlarmManager._alarm_time(alarm2, timepoint))

    def test_once(self):
        timepoint = datetime(day=1, month=3, year=2020, hour=6, minute=13)

        alarm1 = AlarmConfig(waketime='7:15', days=[], enabled=True)        
        self.assertEqual(timepoint.replace(hour=7, minute=15),
            AlarmManager._alarm_time(alarm1, timepoint))

        alarm2 = AlarmConfig(waketime='5:15', days=[], enabled=True)        
        self.assertEqual(timepoint.replace(day=2, hour=5, minute=15),
            AlarmManager._alarm_time(alarm2, timepoint))


    def test_frequently1(self):
        # this is a wednesday, so iso weekday=3
        timepoint = datetime(day=4, month=3, year=2020, hour=6, minute=13)

        # test direct matching day
        alarm1 = AlarmConfig(waketime='7:15', days=[1,2,3,4,5], enabled=True)
        self.assertEqual(timepoint.replace(hour=7, minute=15),
            AlarmManager._alarm_time(alarm1, timepoint))

        # test timepoint has passed today + matching next day
        alarm2 = AlarmConfig(waketime='5:15', days=[1,2,3,4,5], enabled=True)
        self.assertEqual(timepoint.replace(day=5, hour=5, minute=15),
            AlarmManager._alarm_time(alarm2, timepoint))


    def test_frequently2(self):
        # this is a sunday, so iso weekday=7
        timepoint = datetime(day=1, month=3, year=2020, hour=6, minute=13)

        # test direct matching day
        alarm1 = AlarmConfig(waketime='7:15', days=[6,7], enabled=True)        
        self.assertEqual(timepoint.replace(hour=7, minute=15),
            AlarmManager._alarm_time(alarm1, timepoint))

        # test timepoint has passed today + not matching
        alarm2 = AlarmConfig(waketime='5:15', days=[6,7], enabled=True)        
        self.assertEqual(timepoint.replace(day=7, hour=5, minute=15),
            AlarmManager._alarm_time(alarm2, timepoint))


    def test_next_alarm_none(self):
        # this is a sunday, so iso weekday=7
        timepoint = datetime(day=1, month=3, year=2020, hour=6, minute=13)

        # test direct matching day
        alarm_configs_none = [
            AlarmConfig(waketime='7:15', days=[6,7], enabled=False),
            AlarmConfig(waketime='5:12', days=[], enabled=False),
            AlarmConfig(waketime='6:00', days=[1,2,3,4,5], enabled=False),
        ]
        AlarmManager.next_alarm(alarm_configs_none, timepoint)
        self.assertEqual(timepoint.max, AlarmManager.alarm_time)

    def test_next_alarm_once(self):
        # this is a monday, so iso weekday=1
        timepoint = datetime(day=2, month=3, year=2020, hour=6, minute=13)

        # test direct matching day
        alarm_configs_none = [
            AlarmConfig(waketime='7:15', days=[6,7], enabled=True),
            AlarmConfig(waketime='5:12', days=[], enabled=True),
            AlarmConfig(waketime='6:00', days=[1,2,3,4,5], enabled=False),
        ]
        AlarmManager.next_alarm(alarm_configs_none, timepoint)
        self.assertEqual(
            timepoint.replace(day=3, hour=5, minute=12),
            AlarmManager.alarm_time)


    def test_next_alarm_frequent(self):
        # this is a sunday, so iso weekday=7
        timepoint = datetime(day=1, month=3, year=2020, hour=15, minute=13)

        # test direct matching day
        alarm_configs_none = [
            AlarmConfig(waketime='5:15', days=[6,7], enabled=True),
            AlarmConfig(waketime='6:12', days=[], enabled=True),
            AlarmConfig(waketime='6:00', days=[1,2,3,4,5], enabled=True),
        ]
        AlarmManager.next_alarm(alarm_configs_none, timepoint)
        self.assertEqual(
            timepoint.replace(day=2, hour=6, minute=00),
            AlarmManager.alarm_time)

    def test_str_alarm_relative(self):
	# test direct matching day
        alarm_configs_once = [
            AlarmConfig(waketime='6:12', days=[], enabled=True),
        ]
        AlarmManager.next_alarm(alarm_configs_once,
            datetime(day=18, month=3, year=2020, hour=15, minute=13)
        )

        todayalarm = datetime(day=18, month=3, year=2020, hour=6, minute=13)
        self.assertEqual("Today, 06:12",
            AlarmManager.str_alarm_relative(todayalarm)
        )

        tomorrowalarm = datetime(day=17, month=3, year=2020, hour=6, minute=13)
        self.assertEqual("Tomorrow, 06:12",
            AlarmManager.str_alarm_relative(tomorrowalarm)
        )

        dayalarm = datetime(day=15, month=3, year=2020, hour=6, minute=13)
        self.assertEqual("Thursday, 06:12",
            AlarmManager.str_alarm_relative(dayalarm)
        )


    def test_str_alarm_relative_none(self):
	# test direct matching day
        alarm_configs_once = [
            AlarmConfig(waketime='6:12', days=[], enabled=False),
        ]
        AlarmManager.next_alarm(alarm_configs_once,
            datetime(day=18, month=3, year=2020, hour=15, minute=13)
        )

        todayalarm = datetime(day=18, month=3, year=2020, hour=6, minute=13)
        self.assertEqual("",
            AlarmManager.str_alarm_relative(todayalarm)
        )

    def test_is_alarm_now(self):
	# test direct matching day
        alarm_configs_once = [
            AlarmConfig(waketime='6:12', days=[], enabled=True),
        ]
        AlarmManager.next_alarm(alarm_configs_once,
            datetime(day=18, month=3, year=2020, hour=6, minute=13)
        )

        atime = datetime(day=19, month=3, year=2020,
                           hour=6, minute=12, second=44, microsecond=123)
        self.assertTrue(AlarmManager.is_alarm_now(atime))

        atime = datetime(day=19, month=3, year=2020,
                           hour=6, minute=13, second=44, microsecond=123)
        self.assertFalse(AlarmManager.is_alarm_now(atime))

        atime = datetime(day=19, month=3, year=2020,
                           hour=6, minute=11, second=59, microsecond=123)
        self.assertFalse(AlarmManager.is_alarm_now(atime))
