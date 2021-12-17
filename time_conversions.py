'''
time_conversions.py

Module to convert different times to seconds and convert
between different units of time
'''
from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

def minutes_to_seconds( minutes: str ) -> int:
    '''Converts minutes to seconds'''
    return int(minutes)*60

def hours_to_minutes( hours: str ) -> int:
    '''Converts hours to minutes'''
    return int(hours)*60

def hhmm_to_seconds( hhmm: str ) -> int:
    '''converts time from the format hh:mm to a seconds format'''
    if len(hhmm.split(":")) != 2:
        print('Incorrect format. Argument must be formatted as HH:MM')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(":")[0])) + \
        minutes_to_seconds(hhmm.split(":")[1])

def hhmmss_to_seconds( hhmmss: str ) -> int:
    '''converts time from the format hh:mm:ss to a seconds format'''
    if len(hhmmss.split(":")) != 3:
        print('Incorrect format. Argument must be formatted as HH:MM:SS')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmmss.split(":")[0])) + \
        minutes_to_seconds(hhmmss.split(":")[1]) + int(hhmmss.split(":")[2])

def time_till(target_time):
    '''finds the time remaining until a specified time given in format hh:mm'''
    time = hhmm_to_seconds(target_time) - hhmmss_to_seconds(current_time)
    if time<0:
        time+=86400
    return time