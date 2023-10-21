ctypedef pub class Time [type MyTime_Type, object MyTimeObject]:
     cdef pub f64 seconds

ctypedef pub class Event [type MyEvent_Type, object MyEventObject]:
     cdef pub Time time
