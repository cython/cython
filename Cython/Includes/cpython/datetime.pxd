from cpython.object cimport PyObject
from cpython.version cimport PY_VERSION_HEX

cdef extern from "Python.h":
    ctypedef struct PyTypeObject:
        pass

cdef extern from "datetime.h":
    """
    /* Backport for Python 2.x */
    #if PY_MAJOR_VERSION < 3
        #ifndef PyDateTime_DELTA_GET_DAYS
            #define PyDateTime_DELTA_GET_DAYS(o) (((PyDateTime_Delta*)o)->days)
        #endif
        #ifndef PyDateTime_DELTA_GET_SECONDS
            #define PyDateTime_DELTA_GET_SECONDS(o) (((PyDateTime_Delta*)o)->seconds)
        #endif
        #ifndef PyDateTime_DELTA_GET_MICROSECONDS
            #define PyDateTime_DELTA_GET_MICROSECONDS(o) (((PyDateTime_Delta*)o)->microseconds)
        #endif
    #endif

    /* Backport for Python < 3.6 */
    #if PY_VERSION_HEX < 0x030600a4
        #ifndef PyDateTime_TIME_GET_FOLD
            #define PyDateTime_TIME_GET_FOLD(o) ((void)(o), 0)
        #endif
        #ifndef PyDateTime_DATE_GET_FOLD
            #define PyDateTime_DATE_GET_FOLD(o) ((void)(o), 0)
        #endif
    #endif

    /* Backport for Python < 3.6 */
    #if PY_VERSION_HEX < 0x030600a4
        #define __Pyx_DateTime_DateTimeWithFold(year, month, day, hour, minute, second, microsecond, tz, fold) \
            ((void)(fold), PyDateTimeAPI->DateTime_FromDateAndTime(year, month, day, hour, minute, second, \
                microsecond, tz, PyDateTimeAPI->DateTimeType))
        #define __Pyx_DateTime_TimeWithFold(hour, minute, second, microsecond, tz, fold) \
            ((void)(fold), PyDateTimeAPI->Time_FromTime(hour, minute, second, microsecond, tz, PyDateTimeAPI->TimeType))
    #else /* For Python 3.6+ so that we can pass tz */
        #define __Pyx_DateTime_DateTimeWithFold(year, month, day, hour, minute, second, microsecond, tz, fold) \
            PyDateTimeAPI->DateTime_FromDateAndTimeAndFold(year, month, day, hour, minute, second, \
                microsecond, tz, fold, PyDateTimeAPI->DateTimeType)
        #define __Pyx_DateTime_TimeWithFold(hour, minute, second, microsecond, tz, fold) \
            PyDateTimeAPI->Time_FromTimeAndFold(hour, minute, second, microsecond, tz, fold, PyDateTimeAPI->TimeType)
    #endif

    /* Backport for Python < 3.7 */
    #if PY_VERSION_HEX < 0x030700b1
        #define __Pyx_TimeZone_UTC NULL
        #define __Pyx_TimeZone_FromOffsetAndName(offset, name) ((void)(offset), (void)(name), (PyObject*)NULL)
    #else
        #define __Pyx_TimeZone_UTC PyDateTime_TimeZone_UTC
        #define __Pyx_TimeZone_FromOffsetAndName(offset, name) PyTimeZone_FromOffsetAndName(offset, name)
    #endif

    /* Backport for Python < 3.10 */
    #if PY_VERSION_HEX < 0x030a00a1
        #ifndef PyDateTime_TIME_GET_TZINFO
            #define PyDateTime_TIME_GET_TZINFO(o) \
                ((((PyDateTime_Time*)o)->hastzinfo) ? ((PyDateTime_Time*)o)->tzinfo : Py_None)
        #endif
        #ifndef PyDateTime_DATE_GET_TZINFO
            #define PyDateTime_DATE_GET_TZINFO(o) \
                ((((PyDateTime_DateTime*)o)->hastzinfo) ? ((PyDateTime_DateTime*)o)->tzinfo : Py_None)
        #endif
    #endif
    """

    ctypedef extern class datetime.date[object PyDateTime_Date]:
        @property
        fn inline i32 year(self):
            return PyDateTime_GET_YEAR(self)

        @property
        fn inline i32 month(self):
            return PyDateTime_GET_MONTH(self)

        @property
        fn inline i32 day(self):
            return PyDateTime_GET_DAY(self)

    ctypedef extern class datetime.time[object PyDateTime_Time]:
        @property
        fn inline i32 hour(self):
            return PyDateTime_TIME_GET_HOUR(self)

        @property
        fn inline i32 minute(self):
            return PyDateTime_TIME_GET_MINUTE(self)

        @property
        fn inline i32 second(self):
            return PyDateTime_TIME_GET_SECOND(self)

        @property
        fn inline i32 microsecond(self):
            return PyDateTime_TIME_GET_MICROSECOND(self)

        @property
        fn inline object tzinfo(self):
            return <object>PyDateTime_TIME_GET_TZINFO(self)

        @property
        fn inline i32 fold(self):
            # For Python < 3.6 this returns 0 no matter what
            return PyDateTime_TIME_GET_FOLD(self)

    ctypedef extern class datetime.datetime[object PyDateTime_DateTime]:
        @property
        fn inline i32 year(self):
            return PyDateTime_GET_YEAR(self)

        @property
        fn inline i32 month(self):
            return PyDateTime_GET_MONTH(self)

        @property
        fn inline i32 day(self):
            return PyDateTime_GET_DAY(self)

        @property
        fn inline i32 hour(self):
            return PyDateTime_DATE_GET_HOUR(self)

        @property
        fn inline i32 minute(self):
            return PyDateTime_DATE_GET_MINUTE(self)

        @property
        fn inline i32 second(self):
            return PyDateTime_DATE_GET_SECOND(self)

        @property
        fn inline i32 microsecond(self):
            return PyDateTime_DATE_GET_MICROSECOND(self)

        @property
        fn inline object tzinfo(self):
            return <object>PyDateTime_DATE_GET_TZINFO(self)

        @property
        fn inline i32 fold(self):
            # For Python < 3.6 this returns 0 no matter what
            return PyDateTime_DATE_GET_FOLD(self)

    ctypedef extern class datetime.timedelta[object PyDateTime_Delta]:
        @property
        fn inline i32 day(self):
            return PyDateTime_DELTA_GET_DAYS(self)

        @property
        fn inline i32 second(self):
            return PyDateTime_DELTA_GET_SECONDS(self)

        @property
        fn inline i32 microsecond(self):
            return PyDateTime_DELTA_GET_MICROSECONDS(self)

    ctypedef extern class datetime.tzinfo[object PyDateTime_TZInfo]:
        pass

    ctypedef struct PyDateTime_Date:
        pass

    ctypedef struct PyDateTime_Time:
        u8 fold
        char hastzinfo
        PyObject *tzinfo

    ctypedef struct PyDateTime_DateTime:
        u8 fold
        char hastzinfo
        PyObject *tzinfo

    ctypedef struct PyDateTime_Delta:
        i32 days
        i32 seconds
        i32 microseconds

    # Define structure for C API.
    ctypedef struct PyDateTime_CAPI:
        # type objects
        PyTypeObject *DateType
        PyTypeObject *DateTimeType
        PyTypeObject *TimeType
        PyTypeObject *DeltaType
        PyTypeObject *TZInfoType

        # constructors
        date (*Date_FromDate)(i32, i32, i32, PyTypeObject*)
        datetime (*DateTime_FromDateAndTime)(i32, i32, i32, i32, i32, i32, i32, object, PyTypeObject*)
        time (*Time_FromTime)(i32, i32, i32, i32, object, PyTypeObject*)
        timedelta (*Delta_FromDelta)(i32, i32, i32, i32, PyTypeObject*)

        # constructors for the DB API
        datetime (*DateTime_FromTimestamp)(PyObject*, object, PyObject*)
        date (*Date_FromTimestamp)(PyObject*, object)

        # We cannot use the following because they do not compile in older Python versions.
        # Instead, we use datetime.h's macros here that we can backport in C.

        # Python 3.7+ constructors
        object (*TimeZone_FromTimeZone)(object offset, PyObject *name)

        # Python 3.7+ singletons
        PyObject *TimeZone_UTC

        # Python 3.6+ PEP 495 constructors
        datetime (*DateTime_FromDateAndTimeAndFold)(i32, i32, i32, i32, i32, i32, i32, object, i32, PyTypeObject*)
        time (*Time_FromTimeAndFold)(i32, i32, i32 ,i32, object, i32, PyTypeObject*)

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
    i32 PyDateTime_GET_YEAR(object o)
    i32 PyDateTime_GET_MONTH(object o)
    i32 PyDateTime_GET_DAY(object o)

    # Getters for datetime (C macros).
    i32 PyDateTime_DATE_GET_HOUR(object o)
    i32 PyDateTime_DATE_GET_MINUTE(object o)
    i32 PyDateTime_DATE_GET_SECOND(object o)
    i32 PyDateTime_DATE_GET_MICROSECOND(object o)
    i32 PyDateTime_DATE_GET_FOLD(object o)
    PyObject* PyDateTime_DATE_GET_TZINFO(object o)  # returns a borrowed reference

    # Getters for time (C macros).
    i32 PyDateTime_TIME_GET_HOUR(object o)
    i32 PyDateTime_TIME_GET_MINUTE(object o)
    i32 PyDateTime_TIME_GET_SECOND(object o)
    i32 PyDateTime_TIME_GET_MICROSECOND(object o)
    i32 PyDateTime_TIME_GET_FOLD(object o)
    PyObject* PyDateTime_TIME_GET_TZINFO(object o)  # returns a borrowed reference

    # Getters for timedelta (C macros).
    i32 PyDateTime_DELTA_GET_DAYS(object o)
    i32 PyDateTime_DELTA_GET_SECONDS(object o)
    i32 PyDateTime_DELTA_GET_MICROSECONDS(object o)

    # Constructors
    object PyTimeZone_FromOffset(object offset)
    object PyTimeZone_FromOffsetAndName(object offset, object name)

    # The above macros is Python 3.7+ so we use these instead
    object __Pyx_TimeZone_FromOffsetAndName(object offset, PyObject* name)

    # Constructors for the DB API
    datetime PyDateTime_FromTimeStamp(object args)
    date PyDate_FromTimeStamp(object args)

    # PEP 495 constructors but patched above to allow passing tz
    datetime __Pyx_DateTime_DateTimeWithFold(i32, i32, i32, i32, i32, i32, i32, object, i32)
    datetime __Pyx_DateTime_TimeWithFold(i32, i32, i32 ,i32, object, i32)

    # PyDateTime CAPI object.
    PyDateTime_CAPI *PyDateTimeAPI

    PyObject* PyDateTime_TimeZone_UTC

    # PyDateTime_TimeZone_UTC is Python 3.7+ so instead we use the following macro
    PyObject* __Pyx_TimeZone_UTC

    void PyDateTime_IMPORT()

# Datetime C API initialization function.
# You have to call it before any usage of DateTime CAPI functions.
fn inline void import_datetime():
    PyDateTime_IMPORT

# Create date object using DateTime CAPI factory function.
# Note, there are no range checks for any of the arguments.
fn inline date date_new(i32 year, i32 month, i32 day):
    return PyDateTimeAPI.Date_FromDate(year, month, day, PyDateTimeAPI.DateType)

# Create time object using DateTime CAPI factory function
# Note, there are no range checks for any of the arguments.
fn inline time time_new(i32 hour, i32 minute, i32 second, i32 microsecond, object tz, i32 fold=0):
    return __Pyx_DateTime_TimeWithFold(hour, minute, second, microsecond, tz, fold)

# Create datetime object using DateTime CAPI factory function.
# Note, there are no range checks for any of the arguments.
fn inline datetime datetime_new(i32 year, i32 month, i32 day, i32 hour, i32 minute, i32 second, i32 microsecond, object tz, i32 fold=0):
    return __Pyx_DateTime_DateTimeWithFold(year, month, day, hour, minute, second, microsecond, tz, fold)

# Create timedelta object using DateTime CAPI factory function.
# Note, there are no range checks for any of the arguments.
fn inline timedelta timedelta_new(i32 days, i32 seconds, i32 useconds):
    return PyDateTimeAPI.Delta_FromDelta(days, seconds, useconds, 1, PyDateTimeAPI.DeltaType)

# Create timedelta object using DateTime CAPI factory function.
fn inline object timezone_new(object offset, object name=None):
    if PY_VERSION_HEX < 0x030700b1:
        raise RuntimeError('Time zones are not available from the C-API.')
    return __Pyx_TimeZone_FromOffsetAndName(offset, <PyObject*>name if name is not None else NULL)

# Create datetime object using DB API constructor.
fn inline datetime datetime_from_timestamp(timestamp, tz=None):
    return PyDateTimeAPI.DateTime_FromTimestamp(
        <PyObject*>PyDateTimeAPI.DateTimeType, (timestamp, tz) if tz is not None else (timestamp,), NULL)

# Create date object using DB API constructor.
fn inline date date_from_timestamp(timestamp):
    return PyDateTimeAPI.Date_FromTimestamp(<PyObject*>PyDateTimeAPI.DateType, (timestamp,))

# More recognizable getters for date/time/datetime/timedelta.
# There are no setters because datetime.h hasn't them.
# This is because of immutable nature of these objects by design.
# If you would change time/date/datetime/timedelta object you need to recreate.

# Get UTC singleton
fn inline object get_utc():
    if PY_VERSION_HEX < 0x030700b1:
        raise RuntimeError('Time zones are not available from the C-API.')
    return <object>__Pyx_TimeZone_UTC

# Get tzinfo of time
fn inline object time_tzinfo(object o):
    return <object>PyDateTime_TIME_GET_TZINFO(o)

# Get tzinfo of datetime
fn inline object datetime_tzinfo(object o):
    return <object>PyDateTime_DATE_GET_TZINFO(o)

# Get year of date
fn inline i32 date_year(object o):
    return PyDateTime_GET_YEAR(o)

# Get month of date
fn inline i32 date_month(object o):
    return PyDateTime_GET_MONTH(o)

# Get day of date
fn inline i32 date_day(object o):
    return PyDateTime_GET_DAY(o)

# Get year of datetime
fn inline i32 datetime_year(object o):
    return PyDateTime_GET_YEAR(o)

# Get month of datetime
fn inline i32 datetime_month(object o):
    return PyDateTime_GET_MONTH(o)

# Get day of datetime
fn inline i32 datetime_day(object o):
    return PyDateTime_GET_DAY(o)

# Get hour of time
fn inline i32 time_hour(object o):
    return PyDateTime_TIME_GET_HOUR(o)

# Get minute of time
fn inline i32 time_minute(object o):
    return PyDateTime_TIME_GET_MINUTE(o)

# Get second of time
fn inline i32 time_second(object o):
    return PyDateTime_TIME_GET_SECOND(o)

# Get microsecond of time
fn inline i32 time_microsecond(object o):
    return PyDateTime_TIME_GET_MICROSECOND(o)

# Get fold of time
fn inline i32 time_fold(object o):
    # For Python < 3.6 this returns 0 no matter what
    return PyDateTime_TIME_GET_FOLD(o)

# Get hour of datetime
fn inline i32 datetime_hour(object o):
    return PyDateTime_DATE_GET_HOUR(o)

# Get minute of datetime
fn inline i32 datetime_minute(object o):
    return PyDateTime_DATE_GET_MINUTE(o)

# Get second of datetime
fn inline i32 datetime_second(object o):
    return PyDateTime_DATE_GET_SECOND(o)

# Get microsecond of datetime
fn inline i32 datetime_microsecond(object o):
    return PyDateTime_DATE_GET_MICROSECOND(o)

# Get fold of datetime
fn inline i32 datetime_fold(object o):
    # For Python < 3.6 this returns 0 no matter what
    return PyDateTime_DATE_GET_FOLD(o)

# Get days of timedelta
fn inline i32 timedelta_days(object o):
    return (<PyDateTime_Delta*>o).days

# Get seconds of timedelta
fn inline i32 timedelta_seconds(object o):
    return (<PyDateTime_Delta*>o).seconds

# Get microseconds of timedelta
fn inline i32 timedelta_microseconds(object o):
    return (<PyDateTime_Delta*>o).microseconds

fn inline f64 total_seconds(timedelta obj):
    # Mirrors the "timedelta.total_seconds()" method.
    # Note that this implementation is not guaranteed to give *exactly* the same
    # result as the original method, due to potential differences in floating point rounding.
    cdef:
        f64 days, seconds, micros
    days = <f64>PyDateTime_DELTA_GET_DAYS(obj)
    seconds = <f64>PyDateTime_DELTA_GET_SECONDS(obj)
    micros = <f64>PyDateTime_DELTA_GET_MICROSECONDS(obj)
    return days * 24 * 3600 + seconds + micros / 1_000_000
