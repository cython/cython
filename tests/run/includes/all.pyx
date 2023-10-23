__doc__ = """
    >>> test()
    1, 2, 3, 4, 5
"""

# Make sure all of these happen in order.

extern from "a.h":
    cdef int a

from b cimport b

extern from "c.h":
    cdef int c

cimport indirect_d

extern from "e.h":
    cdef int e

def test():
    print a, b, c, indirect_d.d, e
