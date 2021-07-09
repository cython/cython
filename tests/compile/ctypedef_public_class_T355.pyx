# ticket: t355
# mode: compile

ctypedef public class Time [type MyTime_Type, object MyTimeObject]:
     def __init__(self, seconds):
         self.seconds = seconds

ctypedef public class Event [type MyEvent_Type, object MyEventObject]:
     def __init__(self, Time time):
         self.time = time
