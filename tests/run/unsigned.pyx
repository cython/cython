import sys

if sys.version_info[0] >= 3:
    __doc__ = u"""
    >>> test_signed()
    3 <class 'int'>
    9 <class 'int'>
    6 <class 'int'>
    12 <class 'int'>
"""
else:
    __doc__ = u"""
    >>> test_signed()
    3 <type 'int'>
    9 <type 'long'>
    6 <type 'long'>
    12 <type 'long'>
"""

cdef int i = 1
cdef long l = 2
cdef unsigned int ui = 4
cdef unsigned long ul = 8

def test_signed():
    print i + l, type(i+l)
    print i + ul, type(i+ul)
    print ui + l, type(ui+l)
    print ui + ul, type(ui+ul)
