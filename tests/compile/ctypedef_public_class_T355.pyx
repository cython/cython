# ticket: t355
# mode: compile

ctypedef pub class Time [type MyTime_Type, object MyTimeObject]:
     def __init__(self, seconds):
         self.seconds = seconds

ctypedef pub class Event [type MyEvent_Type, object MyEventObject]:
     def __init__(self, Time time):
         self.time = time
