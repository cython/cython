# tag: cpp
# mode: compile

cdef extern from "point.h" namespace "geometry":

    cdef struct Point:
        double x
        double y
        int color

cdef Point p = Point(0.0, 0.0, 0)
the_point = p
