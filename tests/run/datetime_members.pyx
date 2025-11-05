# mode: run
# tag: datetime

from cpython.datetime cimport import_datetime
from cpython.datetime cimport time_new, date_new, datetime_new, timedelta_new
from cpython.datetime cimport datetime, time
from cpython.datetime cimport time_tzinfo, datetime_tzinfo
from cpython.datetime cimport time_hour, time_minute, time_second, time_microsecond, time_tzinfo, time_fold
from cpython.datetime cimport date_day, date_month, date_year
from cpython.datetime cimport datetime_day, datetime_month, datetime_year
from cpython.datetime cimport datetime_hour, datetime_minute, datetime_second, \
                              datetime_microsecond, datetime_tzinfo, datetime_fold
from cpython.datetime cimport timedelta_days, timedelta_seconds, timedelta_microseconds

import_datetime()

def test_date(int year, int month, int day):
    '''
    >>> test_date(2012,12,31)
    (True, True, True)
    '''
    o = date_new(year, month, day)
    return o.year == date_year(o), \
           o.month == date_month(o), \
           o.day == date_day(o)

def test_datetime(int year, int month, int day, int hour,
                  int minute, int second, int microsecond, int fold):
    '''
    >>> test_datetime(2012, 12, 31, 12, 30, 59, 12345, 0)
    (True, True, True, True, True, True, True, True, True)
    >>> test_datetime(2012, 12, 11, 12, 30, 59, 3322, 1)
    (True, True, True, True, True, True, True, True, True)
    '''
    o = datetime_new(
        year, month, day, hour, minute, second, microsecond, None, fold
    )
    return o.year == datetime_year(o), \
           o.month == datetime_month(o), \
           o.day == datetime_day(o), \
           o.hour == datetime_hour(o), \
           o.minute == datetime_minute(o), \
           o.second == datetime_second(o), \
           o.microsecond == datetime_microsecond(o), \
           o.tzinfo == datetime_tzinfo(o), \
           o.fold == datetime_fold(o)

def test_time(int hour, int minute, int second, int microsecond, int fold):
    '''
    >>> test_time(12, 30, 59, 12345, 0)
    (True, True, True, True, True, True)
    >>> test_time(12, 30, 43, 5432, 1)
    (True, True, True, True, True, True)
    '''
    o = time_new(hour, minute, second, microsecond, None, fold)
    return o.hour == time_hour(o), \
           o.minute == time_minute(o), \
           o.second == time_second(o), \
           o.microsecond == time_microsecond(o), \
           o.tzinfo == time_tzinfo(o), \
           o.fold == time_fold(o)

def test_timedelta(int days, int seconds, int microseconds):
    '''
    >>> test_timedelta(30, 1440, 123456)
    (True, True, True)
    '''
    o = timedelta_new(days, seconds, microseconds)
    return o.days == timedelta_days(o), \
           o.seconds == timedelta_seconds(o), \
           o.microseconds == timedelta_microseconds(o)
