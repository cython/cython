from cpython.object cimport PyObject
from cpython.version cimport PY_VERSION_HEX

cdef extern from "Python.h":
    ctypedef struct PyTypeObject:
        pass

cdef extern from "datetime.h":
    """
    /* Backport for Python < 3.3 */
    #ifndef PyDateTime_DELTA_GET_DAYS
        #define PyDateTime_DELTA_GET_DAYS(o) (((PyDateTime_Delta*)o)->days)
    #endif
    #ifndef PyDateTime_DELTA_GET_SECONDS
        #define PyDateTime_DELTA_GET_SECONDS(o) (((PyDateTime_Delta*)o)->seconds)
    #endif
    #ifndef PyDateTime_DELTA_GET_MICROSECONDS
        #define PyDateTime_DELTA_GET_MICROSECONDS(o) (((PyDateTime_Delta*)o)->microseconds)
    #endif

    /* Backport for Python < 3.6 */
    #ifndef PyDateTime_TIME_GET_FOLD
        #define PyDateTime_TIME_GET_FOLD(o) 0
    #endif
    #ifndef PyDateTime_DATE_GET_FOLD
        #define PyDateTime_DATE_GET_FOLD(o) 0
    #endif

    /* Backport for Python < 3.6 */
    #ifndef PyDateTime_FromDateAndTimeAndFold
        #define __Pyx_DateTime_DateTimeWithFold(year, month, day, hour, minute, second, microsecond, tz, fold) \
            PyDateTimeAPI->DateTime_FromDateAndTime(year, month, day, hour, minute, second, \
                microsecond, tz, PyDateTimeAPI->DateTimeType)
    #endif
    #ifndef PyTime_FromTimeAndFold
        #define __Pyx_DateTime_TimeWithFold(hour, minute, second, usecond, tz, fold) \
            PyDateTimeAPI->Time_FromTime(hour, minute, second, usecond, tz, PyDateTimeAPI->TimeType)
    #endif

    /* Define the __Pyx_DateTime macros for Python 3.6+ */
    #ifndef __Pyx_DateTime_DateTimeWithFold
        #define __Pyx_DateTime_DateTimeWithFold(hour, minute, second, usecond, tz, fold) \
            PyDateTimeAPI->DateTime_FromDateAndTimeAndFold(year, month, day, hour, minute, second, \
                microsecond, tz, fold, PyDateTimeAPI->DateTimeType)
    #endif
    #ifndef __Pyx_DateTime_TimeWithFold
        #define __Pyx_DateTime_TimeWithFold(hour, minute, second, usecond, tz, fold) \
            PyDateTimeAPI->Time_FromTimeAndFold(hour, minute, second, usecond, tz, fold, PyDateTimeAPI->TimeType)
    #endif

    /* Backport for Python < 3.7 */
    #ifndef PyDateTime_TimeZone_UTC
        #define PyDateTime_TimeZone_UTC NULL
    #endif
    #ifndef PyTimeZone_FromOffset
        #define PyTimeZone_FromOffset(offset) NULL
    #endif
    #ifndef PyTimeZone_FromOffsetAndName
        #define PyTimeZone_FromOffsetAndName(offset, name) PyTimeZone_FromOffset(offset)
    #endif
    """

    ctypedef extern class datetime.date[object PyDateTime_Date]:
        @property
        cdef inline int year(self):
            return PyDateTime_GET_YEAR(self)

        @property
        cdef inline int month(self):
            return PyDateTime_GET_MONTH(self)

        @property
        cdef inline int day(self):
            return PyDateTime_GET_DAY(self)

    ctypedef extern class datetime.time[object PyDateTime_Time]:
        @property
        cdef inline int hour(self):
            return PyDateTime_TIME_GET_HOUR(self)

        @property
        cdef inline int minute(self):
            return PyDateTime_TIME_GET_MINUTE(self)

        @property
        cdef inline int second(self):
            return PyDateTime_TIME_GET_SECOND(self)

        @property
        cdef inline int microsecond(self):
            return PyDateTime_TIME_GET_MICROSECOND(self)

        @property
        cdef inline int fold(self):
            # For Python < 3.6 this returns 0 no matter what
            return PyDateTime_TIME_GET_FOLD(self)

    ctypedef extern class datetime.datetime[object PyDateTime_DateTime]:
        @property
        cdef inline int year(self):
            return PyDateTime_GET_YEAR(self)

        @property
        cdef inline int month(self):
            return PyDateTime_GET_MONTH(self)

        @property
        cdef inline int day(self):
            return PyDateTime_GET_DAY(self)

        @property
        cdef inline int hour(self):
            return PyDateTime_DATE_GET_HOUR(self)

        @property
        cdef inline int minute(self):
            return PyDateTime_DATE_GET_MINUTE(self)

        @property
        cdef inline int second(self):
            return PyDateTime_DATE_GET_SECOND(self)

        @property
        cdef inline int microsecond(self):
            return PyDateTime_DATE_GET_MICROSECOND(self)

        @property
        cdef inline int fold(self):
            # For Python < 3.6 this returns 0 no matter what
            return PyDateTime_DATE_GET_FOLD(self)

    ctypedef extern class datetime.timedelta[object PyDateTime_Delta]:
        @property
        cdef inline int day(self):
            return PyDateTime_DELTA_GET_DAYS(self)

        @property
        cdef inline int second(self):
            return PyDateTime_DELTA_GET_SECONDS(self)

        @property
        cdef inline int microsecond(self):
            return PyDateTime_DELTA_GET_MICROSECONDS(self)

    ctypedef extern class datetime.tzinfo[object PyDateTime_TZInfo]:
        pass

    ctypedef struct PyDateTime_Date:
        pass

    ctypedef struct PyDateTime_Time:
        unsigned char fold
        char hastzinfo
        PyObject *tzinfo

    ctypedef struct PyDateTime_DateTime:
        unsigned char fold
        char hastzinfo
        PyObject *tzinfo

    ctypedef struct PyDateTime_Delta:
        int days
        int seconds
        int microseconds

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
        object (*DateTime_FromTimestamp)(object, object, PyObject*)
        object (*Date_FromTimestamp)(object, object)

        # We cannot use the following because they do not compile in older Python versions.
        # Instead, we use datetime.h's macros here that we can backport in C.

        # Python 3.7+ constructors
        object (*TimeZone_FromTimeZone)(object offset, PyObject *name)

        # Python 3.7+ singletons
        PyObject *TimeZone_UTC

        # Python 3.6+ PEP 495 constructors
        object (*DateTime_FromDateAndTimeAndFold)(int, int, int, int, int, int, int, object, int, PyTypeObject*)
        object (*Time_FromTimeAndFold)(int, int, int ,int, object, int, PyTypeObject*)

    # Check type of the object.
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

    # Getters for date and datetime (C macros).
    int PyDateTime_GET_YEAR(object o)
    int PyDateTime_GET_MONTH(object o)
    int PyDateTime_GET_DAY(object o)

    # Getters for datetime (C macros).
    int PyDateTime_DATE_GET_HOUR(object o)
    int PyDateTime_DATE_GET_MINUTE(object o)
    int PyDateTime_DATE_GET_SECOND(object o)
    int PyDateTime_DATE_GET_MICROSECOND(object o)
    int PyDateTime_DATE_GET_FOLD(object o)
    object PyDateTime_DATE_GET_TZINFO(object o)

    # Getters for time (C macros).
    int PyDateTime_TIME_GET_HOUR(object o)
    int PyDateTime_TIME_GET_MINUTE(object o)
    int PyDateTime_TIME_GET_SECOND(object o)
    int PyDateTime_TIME_GET_MICROSECOND(object o)
    int PyDateTime_TIME_GET_FOLD(object o)
    object PyDateTime_TIME_GET_TZINFO(object o)

    # Getters for timedelta (C macros).
    int PyDateTime_DELTA_GET_DAYS(object o)
    int PyDateTime_DELTA_GET_SECONDS(object o)
    int PyDateTime_DELTA_GET_MICROSECONDS(object o)

    # Constructors
    object PyTimeZone_FromOffset(object offset)
    object PyTimeZone_FromOffsetAndName(object offset, str name)

    # Constructors for the DB API
    object PyDateTime_FromTimeStamp(object args)
    object PyDate_FromTimeStamp(object args)

    # datetime.h's macros don't allow passing tz so we define our own.
    object __Pyx_DateTime_DateTimeWithFold(int, int, int, int, int, int, int, object, int)
    object __Pyx_DateTime_TimeWithFold(int, int, int ,int, object, int)

    # PyDateTime CAPI object.
    PyDateTime_CAPI *PyDateTimeAPI

    PyObject* PyDateTime_TimeZone_UTC  # Requires Py3.7+ !

    void PyDateTime_IMPORT()

# Datetime C API initialization function.
# You have to call it before any usage of DateTime CAPI functions.
cdef inline void import_datetime():
    PyDateTime_IMPORT

# Create date object using DateTime CAPI factory function.
# Note, there are no range checks for any of the arguments.
cdef inline object date_new(int year, int month, int day):
    return PyDateTimeAPI.Date_FromDate(year, month, day, PyDateTimeAPI.DateType)

# Create time object using DateTime CAPI factory function
# Note, there are no range checks for any of the arguments.
cdef inline object time_new(int hour, int minute, int second, int microsecond, object tz):
    return PyDateTimeAPI.Time_FromTime(hour, minute, second, microsecond, tz, PyDateTimeAPI.TimeType)

# Create datetime object using DateTime CAPI factory function.
# Note, there are no range checks for any of the arguments.
cdef inline object datetime_new(int year, int month, int day, int hour, int minute, int second, int microsecond, object tz):
    return PyDateTimeAPI.DateTime_FromDateAndTime(year, month, day, hour, minute, second, microsecond, tz, PyDateTimeAPI.DateTimeType)

# Create timedelta object using DateTime CAPI factory function.
# Note, there are no range checks for any of the arguments.
cdef inline object timedelta_new(int days, int seconds, int useconds):
    return PyDateTimeAPI.Delta_FromDelta(days, seconds, useconds, 1, PyDateTimeAPI.DeltaType)

# Create datetime object using PEP 495 constructor.
cdef inline object datetime_and_fold_new(
        int year, int month, int day, int hour, int minute, int second, int microsecond, object tz, int fold
    ):
    if PY_VERSION_HEX < 0x030600a4:
        raise RuntimeError('PEP 495 constructors are not available from the C-API.')
    return __Pyx_DateTime_DateTimeWithFold(year, month, day, hour, minute, second, microsecond, tz, fold)

# Create time object using PEP 495 constructor.
cdef inline object time_and_fold_new(int hour, int minute, int second, int microsecond, object tz, int fold):
    if PY_VERSION_HEX < 0x030600a4:
        raise RuntimeError('PEP 495 constructors are not available from the C-API.')
    return __Pyx_DateTime_TimeWithFold(hour, minute, second, microsecond, tz, fold)

cdef inline object timezone_new(object offset, str name=None):
    if PY_VERSION_HEX < 0x030700b1:
        raise RuntimeError('Time zones are not available from the C-API.')
    return PyTimeZone_FromOffsetAndName(offset, name)

# Create datetime object using DB API constructor.
cdef inline object datetime_from_timestamp(timestamp, tz=None):
    return PyDateTimeAPI.DateTime_FromTimestamp(
        <object>PyDateTimeAPI.DateTimeType, (timestamp, tz) if tz is not None else (timestamp,), NULL)

# Create date object using DB API constructor.
cdef inline object date_from_timestamp(timestamp):
    return PyDateTimeAPI.Date_FromTimestamp(<object>PyDateTimeAPI.DateType, (timestamp,))

# More recognizable getters for date/time/datetime/timedelta.
# There are no setters because datetime.h hasn't them.
# This is because of immutable nature of these objects by design.
# If you would change time/date/datetime/timedelta object you need to recreate.

# Get UTC singleton
cdef inline object get_utc():
    if PY_VERSION_HEX < 0x030700b1:
        raise RuntimeError('Time zones are not available from the C-API.')
    return <object>PyDateTime_TimeZone_UTC

# Get tzinfo of time
cdef inline object time_tzinfo(object o):
    if (<PyDateTime_Time*>o).hastzinfo:
        return <object>(<PyDateTime_Time*>o).tzinfo
    else:
        return None

# Get tzinfo of datetime
cdef inline object datetime_tzinfo(object o):
    if (<PyDateTime_DateTime*>o).hastzinfo:
        return <object>(<PyDateTime_DateTime*>o).tzinfo
    else:
        return None

# Get year of date
cdef inline int date_year(object o):
    return PyDateTime_GET_YEAR(o)

# Get month of date
cdef inline int date_month(object o):
    return PyDateTime_GET_MONTH(o)

# Get day of date
cdef inline int date_day(object o):
    return PyDateTime_GET_DAY(o)

# Get year of datetime
cdef inline int datetime_year(object o):
    return PyDateTime_GET_YEAR(o)

# Get month of datetime
cdef inline int datetime_month(object o):
    return PyDateTime_GET_MONTH(o)

# Get day of datetime
cdef inline int datetime_day(object o):
    return PyDateTime_GET_DAY(o)

# Get hour of time
cdef inline int time_hour(object o):
    return PyDateTime_TIME_GET_HOUR(o)

# Get minute of time
cdef inline int time_minute(object o):
    return PyDateTime_TIME_GET_MINUTE(o)

# Get second of time
cdef inline int time_second(object o):
    return PyDateTime_TIME_GET_SECOND(o)

# Get microsecond of time
cdef inline int time_microsecond(object o):
    return PyDateTime_TIME_GET_MICROSECOND(o)

# Get fold of time
cdef inline int time_fold(object o):
    # For Python < 3.6 this returns 0 no matter what
    return PyDateTime_DATE_GET_FOLD(o)

# Get hour of datetime
cdef inline int datetime_hour(object o):
    return PyDateTime_DATE_GET_HOUR(o)

# Get minute of datetime
cdef inline int datetime_minute(object o):
    return PyDateTime_DATE_GET_MINUTE(o)

# Get second of datetime
cdef inline int datetime_second(object o):
    return PyDateTime_DATE_GET_SECOND(o)

# Get microsecond of datetime
cdef inline int datetime_microsecond(object o):
    return PyDateTime_DATE_GET_MICROSECOND(o)

# Get fold of datetime
cdef inline int datetime_fold(object o):
    # For Python < 3.6 this returns 0 no matter what
    return PyDateTime_DATE_GET_FOLD(o)

# Get days of timedelta
cdef inline int timedelta_days(object o):
    return (<PyDateTime_Delta*>o).days

# Get seconds of timedelta
cdef inline int timedelta_seconds(object o):
    return (<PyDateTime_Delta*>o).seconds

# Get microseconds of timedelta
cdef inline int timedelta_microseconds(object o):
    return (<PyDateTime_Delta*>o).microseconds

cdef inline double total_seconds(timedelta obj):
    # Mirrors the "timedelta.total_seconds()" method.
    # Note that this implementation is not guaranteed to give *exactly* the same
    # result as the original method, due to potential differences in floating point rounding.
    cdef:
        double days, seconds, micros
    days = <double>PyDateTime_DELTA_GET_DAYS(obj)
    seconds = <double>PyDateTime_DELTA_GET_SECONDS(obj)
    micros = <double>PyDateTime_DELTA_GET_MICROSECONDS(obj)
    return days * 24 * 3600 + seconds + micros / 1_000_000
