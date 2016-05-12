# tag: cpp
# mode: compile

from cython.view import array

cdef extern from "point.h" namespace "geometry":

    cdef struct Point:
        double x
        double y
        int color

cdef Point p = Point(0.0, 0.0, 0)
the_point = p

cdef Point[::1] ps = array((10,), itemsize=sizeof(Point), format='ddi')
