from cpython.ref cimport PyObject

cdef extern from "Python.h":
    PyObject *Py_None
    ctypedef struct PyTypeObject:
        pass

cdef extern from "datetime.h":
    
    ctypedef class datetime.date[object PyDateTime_Date]:
        pass

    ctypedef class datetime.time[object PyDateTime_Time]:
        pass

    ctypedef class datetime.datetime[object PyDateTime_DateTime]:
        pass

    ctypedef class datetime.timedelta[object PyDateTime_Delta]:
        pass

    ctypedef class datetime.tzinfo[object PyDateTime_TZInfo]:
        pass

    ctypedef struct PyDateTime_Date:
        pass
    
    ctypedef struct PyDateTime_Time:
        char hastzinfo             # boolean flag
        PyObject *tzinfo
        
    ctypedef struct PyDateTime_DateTime:
        char hastzinfo             # boolean flag
        PyObject *tzinfo
        
    # Define structure for C API.
    ctypedef struct PyDateTime_CAPI:
        # type objects 
        PyTypeObject *DateType
        PyTypeObject *DateTimeType
        PyTypeObject *TimeType
        PyTypeObject *DeltaType
        PyTypeObject *TZInfoType
    
        # constructors
        object (*Date_FromDate)(int, int, int, PyTypeObject*)
        object (*DateTime_FromDateAndTime)(int, int, int, int, int, int, int, object, PyTypeObject*)
        object (*Time_FromTime)(int, int, int, int, object, PyTypeObject*)
        object (*Delta_FromDelta)(int, int, int, int, PyTypeObject*)
    
        # constructors for the DB API
        object (*DateTime_FromTimestamp)(object, object, object)
        object (*Date_FromTimestamp)(object, object)
    
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


    # PyDateTime CAPI object
    PyDateTime_CAPI *PyDateTimeAPI
    
    #
    # Datetime C API object initialization C macros
    # You have to call this before any usage of DateTime CAPI functions:
    #   PyDateTime_IMPORT
    #
    void PyDateTime_IMPORT()

# Create date object using DateTime CAPI factory function
# Note, there are no range checks for any of the arguments.
cdef inline object date_new(int year, int month, int day):
    return PyDateTimeAPI.Date_FromDate(year, month, day, PyDateTimeAPI.DateType)
    
# Create time object using DateTime CAPI factory function
# Note, there are no range checks for any of the arguments.
cdef inline object time_new(int hour, int minute, int second, int microsecond, object tz):
    return PyDateTimeAPI.Time_FromTime(hour, minute, second, microsecond, tz, PyDateTimeAPI.TimeType)

# Create datetime object using DateTime CAPI factory function
# Note, there are no range checks for any of the arguments.
cdef inline object datetime_new(int year, int month, int day, int hour, int minute, int second, int microsecond, object tz):
    return PyDateTimeAPI.DateTime_FromDateAndTime(year, month, day, hour, minute, second, microsecond, tz, PyDateTimeAPI.DateTimeType)

# Create timedelta object using DateTime CAPI factory function
# Note, there are no range checks for any of the arguments.
cdef inline object timedelta_new(int days, int seconds, int useconds):
    return PyDateTimeAPI.Delta_FromDelta(days, seconds, useconds, 1, PyDateTimeAPI.DeltaType)

