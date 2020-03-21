from datetime import datetime, timedelta


class AlarmManager:

    alarm_time   = datetime.max
    alarm_config = None 

    @staticmethod
    def _alarm_time(alarmconfig, timepoint):
        if alarmconfig.enabled:
            # compute next alarm time relative to timepoint
            alarm_dt = timepoint.replace(
                hour=alarmconfig.waketime.hour,
                minute=alarmconfig.waketime.minute,
                second=0)
            # if next alarm is in the past relative to timepoint 
            if alarm_dt <= timepoint:
                alarm_dt += timedelta(days=1)
            # check whether it applies to config
            if not alarmconfig.days:
                # one alarm
                return alarm_dt
            else:
                # find the weekday closest to the earliest next alarm time
                # using iso week days starting with 1 in alarmconfig                
                daydistance = min(
                    map(lambda day: (day-alarm_dt.isoweekday())%7,
                        alarmconfig.days))
                return alarm_dt + timedelta(days=daydistance)                    
        
        # return the maximal supported time to support earliest time
        # search with min 
        return datetime.max


    @classmethod
    def next_alarm(cls, alarmconfigs, timepoint):
        """Compute the next alarm time given the configuration rules and
           the current timepoint"""
        alarm = min(  
            map(lambda config:
                    (AlarmManager._alarm_time(config, timepoint=timepoint),
                    config), 
                alarmconfigs),
            key = lambda t: t[0], 
            default=(datetime.max, None))
        cls.alarm_time   = alarm[0]
        cls.alarm_config = alarm[1]

    @classmethod
    def str_alarm_relative(cls, timepoint, locale="", 
           dayformat="%A", timeformat="%H:%M"):
        """Give a pretty interpretation of the next alarm relative to timepoint,
           e.g. today, tomorrow, Monday, ..."""
        # never a next alarm set
        if cls.alarm_time == datetime.max:
            return "" 

        days_to_alarm = (cls.alarm_time - timepoint).days
        if days_to_alarm == 0:
            return cls.alarm_time.strftime("Today, " + timeformat) 
        elif days_to_alarm == 1:
            return cls.alarm_time.strftime("Tomorrow, " + timeformat) 
        else:
            # days_to_alarm is implicitly always < 7 at the moment:
            return cls.alarm_time.strftime( dayformat + ", " + timeformat) 
        #  else:
        #    return cls.alarm.strftime(dateformat + ", " + timeformat)

    @classmethod
    def is_alarm_now(cls, timepoint):
        # reduce precision before alarm comparision
        timepoint_minute = timepoint.replace(second=0, microsecond=0)
        if timepoint_minute == cls.alarm_time:
            # only alarm if method is called within the same minute
            return True
        else:
            return False
