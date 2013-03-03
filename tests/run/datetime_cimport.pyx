# coding: utf-8

from cpython.datetime cimport import_datetime
from cpython.datetime cimport date, time, datetime, timedelta, PyDateTime_IMPORT

import_datetime()
        
def test_date(int year, int month, int day):
    '''
    >>> val = test_date(2012, 12, 31)
    >>> print(val)
    2012-12-31
    '''
    val = date(year, month, day)
    return val

def test_time(int hour, int minute, int second, int microsecond):
    '''
    >>> val = test_time(12, 20, 55, 0)
    >>> print(val)
    12:20:55
    '''
    val = time(hour, minute, second, microsecond)
    return val

def test_datetime(int year, int month, int day, int hour, int minute, int second, int microsecond):
    '''
    >>> val = test_datetime(2012, 12, 31, 12, 20, 55, 0)
    >>> print(val)
    2012-12-31 12:20:55
    '''
    val = datetime(year, month, day, hour, minute, second, microsecond)
    return val

def test_timedelta(int days, int seconds, int useconds):
    '''
    >>> val = test_timedelta(30, 0, 0)
    >>> print(val)
    30 days, 0:00:00
    '''
    val = timedelta(days, seconds, useconds)
    return val
