ctypedef public class Time [type MyTime_Type, object MyTimeObject]:
     cdef public double seconds

ctypedef public class Event [type MyEvent_Type, object MyEventObject]:
     cdef public Time time
