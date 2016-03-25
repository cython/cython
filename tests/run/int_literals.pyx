# mode: run
# tag: syntax

from __future__ import absolute_import

cimport cython
from cython cimport typeof

import sys


def valid_underscore_literals():
    """
    >>> valid_underscore_literals()
    """
    # Copied from CPython's test_grammar.py
    assert 0_0_0 == 0
    assert 4_2 == 42
    assert 1_0000_0000 == 100000000
    assert 0b1001_0100 == 0b10010100
    assert 0xffff_ffff == 0xffffffff
    assert 0o5_7_7 == 0o577
    assert 1_00_00.5 == 10000.5
    assert 1e1_0 == 1e10
    assert .1_4 == .14
    assert 1_0 == 1_0L == 1_0LL == 1_0UL == 1_0ULL
    assert typeof(1_0ULL) == "unsigned long long"


@cython.test_assert_path_exists(
    '//IntNode[@longness = "LL"]',
    '//IntNode[@longness = "L"]',
    )
@cython.test_fail_if_path_exists('//IntNode[@longness = ""]')
def c_longs():
    """
    >>> c_longs() == (1, 1, -1, 18446744073709551615)  or  c_longs()
    True
    """
    cdef long a = 1L
    cdef unsigned long ua = 1UL
    cdef long long aa = 0xFFFFFFFFFFFFFFFFLL
    cdef unsigned long long uaa = 0xFFFFFFFFFFFFFFFFULL
    return a, ua, int(aa), uaa

@cython.test_assert_path_exists(
    '//IntNode[@longness = "LL"]',
    '//IntNode[@longness = "L"]',
    )
@cython.test_fail_if_path_exists('//IntNode[@longness = ""]')
def negative_c_longs():
    """
    >>> negative_c_longs() == (-1, -9223285636854775809)  or  negative_c_longs()
    True
    """
    cdef long a = -1L
    cdef long long aa = -9223285636854775809LL
    return a, aa

def py_longs():
    """
    >>> py_longs() == (
    ...     1, 1, 100000000000000000000000000000000, -100000000000000000000000000000000
    ...     )  or  py_longs()
    True
    """
    return 1, 1L, 100000000000000000000000000000000, -100000000000000000000000000000000

@cython.test_fail_if_path_exists("//NumBinopNode", "//IntBinopNode")
@cython.test_assert_path_exists("//ReturnStatNode/IntNode")
def py_huge_calculated_long():
    """
    >>> py_huge_calculated_long() == (
    ...     1606938044258990275541962092341162602522202993782792835301376
    ...     )  or  py_huge_calculated_long()
    True
    """
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
    """
    >>> py_huge_computation_small_result_neg() == (
    ...    -2535301200456458802993406410752, -2535301200456458802993406410752
    ...    )  or  py_huge_computation_small_result_neg()
    True
    """
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
