# coding: utf-8

cimport cpython.datetime
from cpython.datetime cimport PyDateTime_IMPORT
from cpython.datetime cimport PyTime_FromTime, \
                              PyDelta_FromDSU, \
                              PyDate_FromDate, \
                              PyDateTime_FromDateAndTime

PyDateTime_IMPORT

#True, True, True, True, True, True, True

def do_datetime(
        int year, int month, int day, 
        int hours, int minutes, int seconds, int microseconds):

    """
    >>> print(do_datetime(2012, 12, 31, 12, 23, 0, 0))
    2012-12-31 12:23:00
    """
    dt = PyDateTime_FromDateAndTime(
        year, month, day, hours, minutes, seconds, microseconds)
    return dt
