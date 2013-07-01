__doc__ = u"""
>>> c_longs()
(1, 1L, -1L, 18446744073709551615L)
>>> negative_c_longs()
(-1, -9223285636854775809L)
>>> py_longs()
(1, 1L, 100000000000000000000000000000000L, -100000000000000000000000000000000L)

>>> py_huge_calculated_long()
1606938044258990275541962092341162602522202993782792835301376L
>>> py_huge_computation_small_result_neg()
(-2535301200456458802993406410752L, -2535301200456458802993406410752L)
"""

cimport cython
from cython cimport typeof

import sys

if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u'L', u'')

@cython.test_assert_path_exists(
    '//IntNode[@longness = "LL"]',
    '//IntNode[@longness = "L"]',
    )
@cython.test_fail_if_path_exists('//IntNode[@longness = ""]')
def c_longs():
    cdef long a = 1L
    cdef unsigned long ua = 1UL
    cdef long long aa = 0xFFFFFFFFFFFFFFFFLL
    cdef unsigned long long uaa = 0xFFFFFFFFFFFFFFFFULL
    return a, ua, aa, uaa

@cython.test_assert_path_exists(
    '//IntNode[@longness = "LL"]',
    '//IntNode[@longness = "L"]',
    )
@cython.test_fail_if_path_exists('//IntNode[@longness = ""]')
def negative_c_longs():
    cdef long a = -1L
    cdef long long aa = -9223285636854775809LL
    return a, aa

def py_longs():
    return 1, 1L, 100000000000000000000000000000000, -100000000000000000000000000000000

@cython.test_fail_if_path_exists("//NumBinopNode", "//IntBinopNode")
@cython.test_assert_path_exists("//ReturnStatNode/IntNode")
def py_huge_calculated_long():
    return 1 << 200

@cython.test_fail_if_path_exists("//NumBinopNode", "//IntBinopNode")
@cython.test_assert_path_exists("//ReturnStatNode/IntNode")
def py_huge_computation_small_result():
    """
    >>> py_huge_computation_small_result()
    2
    """
    return (1 << 200) >> 199

@cython.test_fail_if_path_exists("//NumBinopNode", "//IntBinopNode")
#@cython.test_assert_path_exists("//ReturnStatNode/IntNode")
def py_huge_computation_small_result_neg():
    return -(2 ** 101), (-2) ** 101

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
    (1, -17, 63)
    """
    cdef int a = 0o01
    cdef int b = -0o21
    cdef int c = 0o77
    return a,b,c

def c_oct_py2_legacy():
    """
    >>> c_oct_py2_legacy()
    (1, -17, 63)
    """
    cdef int a = 001
    cdef int b = -021
    cdef int c = 077
    return a,b,c

def py_oct():
    """
    >>> py_oct()
    (1, -17, 63)
    """
    return 0o01, -0o21, 0o77

def py_oct_py2_legacy():
    """
    >>> py_oct_py2_legacy()
    (1, -17, 63)
    """
    return 001, -021, 077

def c_hex():
    """
    >>> c_hex()
    (1, -33, 255)
    """
    cdef int a = 0x01
    cdef int b = -0x21
    cdef int c = 0xFF
    return a,b,c

def py_hex():
    """
    >>> py_hex()
    (1, -33, 255)
    """
    return 0x01, -0x21, 0xFF

def c_bin():
    """
    >>> c_bin()
    (1, -2, 15)
    """
    cdef int a = 0b01
    cdef int b = -0b10
    cdef int c = 0b1111
    return a,b,c

def py_bin():
    """
    >>> py_bin()
    (1, -2, 15)
    """
    return 0b01, -0b10, 0b1111
