/////////////// DatetimeAPI.proto ///////////////

#include "datetime.h"

#define PyDateTime_FromDateAndTimeEx(year, month, day, hour, min, sec, usec, tzinfo) \
    PyDateTimeAPI->DateTime_FromDateAndTime(year, month, day, hour, \
        min, sec, usec, tzinfo, PyDateTimeAPI->DateTimeType)

#define PyTime_FromTimeEx(hour, minute, second, usecond, tzinfo) \
    PyDateTimeAPI->Time_FromTime(hour, minute, second, usecond, \
        tzinfo, PyDateTimeAPI->TimeType)

