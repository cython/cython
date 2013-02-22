from cpython.ref cimport PyObject

cdef extern from "datetime.h":
    
    ctypedef struct PyDateTime_Time:
        char hastzinfo             # boolean flag
        PyObject *tzinfo
        
    ctypedef struct PyDateTime_DateTime:
        char hastzinfo             # boolean flag
        PyObject *tzinfo

    bint PyDate_Check(object op)
    bint PyDate_CheckExact(object op)

    bint PyDateTime_Check(object op)
    bint PyDateTime_CheckExact(object op)

    bint PyTime_Check(object op)
    bint PyTime_CheckExact(object op)

    bint PyDelta_Check(object op)
    bint PyDelta_CheckExact(object op)

    bint PyTZInfo_Check(object op)
    bint PyTZInfo_CheckExact(object op)

    # Apply for date and datetime instances (C macros)
    int PyDateTime_GET_YEAR(object o)
    int PyDateTime_GET_MONTH(object o)
    int PyDateTime_GET_DAY(object o)

    int PyDateTime_DATE_GET_HOUR(object o)
    int PyDateTime_DATE_GET_MINUTE(object o)
    int PyDateTime_DATE_GET_SECOND(object o)
    int PyDateTime_DATE_GET_MICROSECOND(object o)

    # Apply for time instances  (C macros)
    int PyDateTime_TIME_GET_HOUR(object o)
    int PyDateTime_TIME_GET_MINUTE(object o)
    int PyDateTime_TIME_GET_SECOND(object o)
    int PyDateTime_TIME_GET_MICROSECOND(object o)

    # Apply for time delta instances (C macros)
    int PyDateTime_DELTA_GET_DAYS(object o)
    int PyDateTime_DELTA_GET_SECONDS(object o)
    int PyDateTime_DELTA_GET_MICROSECONDS(object o)

    # Datetime C API object initialization macros.
    # You have to call them after first import of datetime module.
    void PyDateTime_IMPORT()
    
    #
    # Datetime C API factory functions.
    # Warning: There are no range check for any of the arguments.
    #
    object PyTime_FromTime(
                int hours, int minutes, int seconds, int microseconds)

    object PyDelta_FromDSU(int days, int seconds, int microseconds)

    object PyDate_FromDate(int year, int month, int day)

    object PyDateTime_FromDateAndTime(
                int year, int month, int day, 
                int hours, int minutes, int seconds, int microseconds)

cdef inline object PyTime_FromTimeEx(
        int hours, int minutes, int seconds, int microseconds, object tzinfo):
        
    val = PyTime_FromTime(hours, minutes, seconds, microseconds)
    if tzinfo is not None:
        (<PyDateTime_Time*>val)[0].hastzinfo = 1
        (<PyDateTime_Time*>val)[0].tzinfo = <PyObject*>tzinfo
    return val

cdef inline object PyTime_FromDateAndTimeEx(
        int year, int month, int day, 
        int hours, int minutes, int seconds, int microseconds, object tzinfo):
        
    val = PyDateTime_FromDateAndTime(
            year, month, day, hours, minutes, seconds, microseconds)
    if tzinfo is not None:
        (<PyDateTime_DateTime*>val)[0].hastzinfo = 1
        (<PyDateTime_DateTime*>val)[0].tzinfo = <PyObject*>tzinfo
    return val
    
