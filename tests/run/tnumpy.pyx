# cannot be named "numpy" in order to not clash with the numpy module!

cimport numpy

try:
    import numpy
    __doc__ = """

    >>> basic()
    [[0 1 2 3 4]
     [5 6 7 8 9]]
    2 0 9 5

    >>> three_dim()
    [[[  0.   1.   2.   3.]
      [  4.   5.   6.   7.]]

     [[  8.   9.  10.  11.]
      [ 12.  13.  14.  15.]]

     [[ 16.  17.  18.  19.]
      [ 20.  21.  22.  23.]]]
    6.0 0.0 13.0 8.0
    
    >>> tnumpy.obj_array()
    [a 1 {}]
    a 1 {}
"""
except:
    __doc__ = ""

def basic():
    cdef object[int, 2] buf = numpy.arange(10, dtype='i').reshape((2, 5))
    print buf
    print buf[0, 2], buf[0, 0], buf[1, 4], buf[1, 0]

def three_dim():
    cdef object[double, 3] buf = numpy.arange(24, dtype='d').reshape((3,2,4))
    print buf
    print buf[0, 1, 2], buf[0, 0, 0], buf[1, 1, 1], buf[1, 0, 0]

def obj_array():
    cdef object[object, 1] buf = numpy.array(["a", 1, {}])
    print buf
    print buf[0], buf[1], buf[2]
