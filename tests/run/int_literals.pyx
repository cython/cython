__doc__ = u"""
>>> c_longs()
(1, 1L, -1L, 18446744073709551615L)
>>> py_longs()
(1, 1L, 100000000000000000000000000000000L, -100000000000000000000000000000000L)
"""

import sys
from cython cimport typeof

if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u'L', u'')

import sys

if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u'L', u'')

def c_longs():
    cdef long a = 1L
    cdef unsigned long ua = 1UL
    cdef long long aa = 0xFFFFFFFFFFFFFFFFLL
    cdef unsigned long long uaa = 0xFFFFFFFFFFFFFFFFULL
    
    return a, ua, aa, uaa
    
def py_longs():
    return 1, 1L, 100000000000000000000000000000000, -100000000000000000000000000000000

def large_literal():
    """
    >>> type(large_literal()) is int
    True
    """
    if sys.version_info[0] >= 3 or sys.maxint > 0xFFFFFFFFFFFF:
        return 0xFFFFFFFFFFFF
    else:
        return 0xFFFFFFF

def c_long_types():
    """
    >>> c_long_types()
    long
    long
    long long
    unsigned long
    unsigned long
    unsigned long long
    """
    print typeof(1)
    print typeof(1L)
    print typeof(1LL)
    print typeof(1U)
    print typeof(1UL)
    print typeof(1ULL)

# different ways to write an integer in Python

def c_oct():
    """
    >>> c_oct()
    (1, 17, 63)
    """
    cdef int a = 0o01
    cdef int b = 0o21
    cdef int c = 0o77
    return a,b,c

def py_oct():
    """
    >>> py_oct()
    (1, 17, 63)
    """
    return 0o01, 0o21, 0o77

def c_hex():
    """
    >>> c_hex()
    (1, 33, 255)
    """
    cdef int a = 0x01
    cdef int b = 0x21
    cdef int c = 0xFF
    return a,b,c

def py_hex():
    """
    >>> py_hex()
    (1, 33, 255)
    """
    return 0x01, 0x21, 0xFF

def c_bin():
    """
    >>> c_bin()
    (1, 2, 15)
    """
    cdef int a = 0b01
    cdef int b = 0b10
    cdef int c = 0b1111
    return a,b,c

def py_bin():
    """
    >>> py_bin()
    (1, 2, 15)
    """
    return 0b01, 0b10, 0b1111
