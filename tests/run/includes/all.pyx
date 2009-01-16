__doc__ = """
    >>> test()
    1, 2, 3, 4, 5
"""

# Make sure all of these happen in order.

cdef extern from "a.h":
    cdef int a

from b cimport b

cdef extern from "c.h":
    cdef int c

from indirect_d cimport d

cdef extern from "e.h":
    cdef int e

def test():
    print a, b, c, d, e
