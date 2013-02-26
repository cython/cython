# coding: utf-8

#cimport cpython.datetime as cy_datetime
#from datetime import time, date, datetime, timedelta, tzinfo


from cpython.datetime cimport PyDateTime_IMPORT
from cpython.datetime cimport time_new, date_new, datetime_new, timedelta_new

import datetime as py_datetime

PyDateTime_IMPORT

ZERO = py_datetime.timedelta(0)

#
# Simple class from datetime docs
#
class FixedOffset(py_datetime.tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset, name):
        self._offset = py_datetime.timedelta(minutes = offset)
        self._name = name

    def utcoffset(self, dt):
        return self._offset

    def tzname(self, dt):
        return self._name

    def dst(self, dt):
        return ZERO
        
def do_date(int year, int month, int day):
    """
    >>> do_date(2012, 12, 31)
    (True, True, True, True)
    """
    v = date_new(year, month, day)
    return type(v) is py_datetime.date, v.year == year, v.month == month, v.day == day

def do_datetime(int year, int month, int day, 
        int hour, int minute, int second, int microsecond):
    """
    >>> do_datetime(2012, 12, 31, 12, 23, 0, 0)
    (True, True, True, True, True, True, True, True, True)
    """
    v = datetime_new(year, month, day, hour, minute, second, microsecond, None)
    return type(v) is py_datetime.datetime, v.year == year, v.month == month, v.day == day, \
           v.hour == hour, v.minute == minute, v.second == second, \
           v.microsecond == microsecond, v.tzinfo is None

def do_time(int hour, int minute, int second, int microsecond):
    """
    >>> do_time(12, 23, 0, 0)
    (True, True, True, True, True, True)
    """
    v = time_new(hour, minute, second, microsecond, None)
    return type(v) is py_datetime.time, \
           v.hour == hour, v.minute == minute, v.second == second, \
           v.microsecond == microsecond, v.tzinfo is None

def do_time_tzinfo(int hour, int minute, int second, int microsecond, object tz):
    """
    >>> tz = FixedOffset(60*3, 'Moscow')    
    >>> do_time_tzinfo(12, 23, 0, 0, tz)
    (True, True, True, True, True, True)
    """
    v = time_new(hour, minute, second, microsecond, tz)
    return type(v) is py_datetime.time, \
           v.hour == hour, v.minute == minute, v.second == second, \
           v.microsecond == microsecond, v.tzinfo is tz


def do_datetime_tzinfo(int year, int month, int day, 
        int hour, int minute, int second, int microsecond, object tz):
    """
    >>> tz = FixedOffset(60*3, 'Moscow')    
    >>> do_datetime_tzinfo(2012, 12, 31, 12, 23, 0, 0, tz)
    (True, True, True, True, True, True, True, True, True)
    """
    v = datetime_new(year, month, day, hour, minute, second, microsecond, tz)
    return type(v) is py_datetime.datetime, v.year == year, v.month == month, v.day == day, \
           v.hour == hour, v.minute == minute, v.second == second, \
           v.microsecond == microsecond, v.tzinfo is tz
           
#def do_time_getset_tzinfo(int hour, int minute, int second, int microsecond, object tz):
#    """
#    >>> tz = FixedOffset(60*3, 'Moscow')    
#    >>> do_time_getset_tzinfo(12, 23, 0, 0, tz)
#    (True, True, True, True)
#    """
#    v = PyTime_FromTime(hour, minute, second, microsecond)
#    PyDateTime_Time_SetTZInfo(v, tz)
#    r1 = (v.tzinfo == tz)
#    r2 = (tz == PyDateTime_Time_GetTZInfo(v))
#    PyDateTime_Time_SetTZInfo(v, None)
#    r3 = (v.tzinfo == None)
#    r4 = (tz == PyDateTime_Time_GetTZInfo(v))
#    return r1, r2, r3, r4
