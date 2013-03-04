# coding: utf-8

#cimport cpython.datetime as cy_datetime
#from datetime import time, date, datetime, timedelta, tzinfo


from cpython.datetime cimport import_datetime
from cpython.datetime cimport time_new, date_new, datetime_new, timedelta_new
from cpython.datetime cimport time_tzinfo, datetime_tzinfo
from cpython.datetime cimport time_hour, time_minute, time_second, time_microsecond
from cpython.datetime cimport date_day, date_month, date_year
from cpython.datetime cimport datetime_day, datetime_month, datetime_year
from cpython.datetime cimport datetime_hour, datetime_minute, datetime_second, \
                              datetime_microsecond

import datetime as py_datetime

import_datetime()

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
           
def do_time_tzinfo2(int hour, int minute, int second, int microsecond, object tz):
    """
    >>> tz = FixedOffset(60*3, 'Moscow')    
    >>> do_time_tzinfo2(12, 23, 0, 0, tz)
    (True, True, True, True, True, True, True, True)
    """
    v = time_new(hour, minute, second, microsecond, None)
    v1 = time_new(
            time_hour(v), 
            time_minute(v), 
            time_second(v), 
            time_microsecond(v), 
            tz)
    r1 = (v1.tzinfo == tz)
    r2 = (tz == time_tzinfo(v1))
    v2 = time_new(
            time_hour(v1), 
            time_minute(v1), 
            time_second(v1), 
            time_microsecond(v1), 
            None)
    r3 = (v2.tzinfo == None)
    r4 = (None == time_tzinfo(v2))
    v3 = time_new(
            time_hour(v2), 
            time_minute(v2), 
            time_second(v2), 
            time_microsecond(v2), 
            tz)
    r5 = (v3.tzinfo == tz)
    r6 = (tz == time_tzinfo(v3))
    r7 = (v2 == v)
    r8 = (v3 == v1)
    return r1, r2, r3, r4, r5, r6, r7, r8


def do_datetime_tzinfo2(int year, int month, int day,
                              int hour, int minute, int second, int microsecond, object tz):
    """
    >>> tz = FixedOffset(60*3, 'Moscow')    
    >>> do_datetime_tzinfo2(2012, 12, 31, 12, 23, 0, 0, tz)
    (True, True, True, True, True, True, True, True)
    """
    v = datetime_new(year, month, day, hour, minute, second, microsecond, None)
    v1 = datetime_new(
            datetime_year(v), 
            datetime_month(v), 
            datetime_day(v), 
            datetime_hour(v), 
            datetime_minute(v), 
            datetime_second(v), 
            datetime_microsecond(v), 
            tz)
    r1 = (v1.tzinfo == tz)
    r2 = (tz == datetime_tzinfo(v1))
    v2 = datetime_new(
            datetime_year(v1), 
            datetime_month(v1), 
            datetime_day(v1), 
            datetime_hour(v1), 
            datetime_minute(v1), 
            datetime_second(v1), 
            datetime_microsecond(v1), 
            None)
    r3 = (v2.tzinfo == None)
    r4 = (None == datetime_tzinfo(v2))
    v3 = datetime_new(
            datetime_year(v2), 
            datetime_month(v2), 
            datetime_day(v2), 
            datetime_hour(v2), 
            datetime_minute(v2), 
            datetime_second(v2), 
            datetime_microsecond(v2), 
            tz)
    r5 = (v3.tzinfo == tz)
    r6 = (tz == datetime_tzinfo(v3))
    r7 = (v2 == v)
    r8 = (v3 == v1)
    return r1, r2, r3, r4, r5, r6, r7, r8
