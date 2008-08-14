# cannot be named "numpy" in order to no clash with the numpy module!

cimport numpy

try:
    import numpy
    __doc__ = """

    >>> basic()
    [[0 1 2 3 4]
     [5 6 7 8 9]]
    2 0 9 5


"""
except:
    __doc__ = ""

def basic():
    cdef object[int, 2] buf = numpy.arange(10).reshape((2, 5))
    print buf
    print buf[0, 2], buf[0, 0], buf[1, 4], buf[1, 0]
