
cimport cython

__doc__ = u"""
    >>> s()
    b'spam'
"""

import sys
if sys.version_info[0] < 3:
    __doc__ = __doc__.replace(u" b'", u" '")


DEF TUPLE = (1, 2, u"buckle my shoe")
DEF TRUE_FALSE = (True, False)
DEF NONE = None

DEF CHAR = c'x'
DEF INT0 = -1
DEF INT1 = 42
DEF INT2 = 0x42
DEF INT3 = -0x42
DEF LONG = 666L
DEF FLOAT = 12.5
DEF STR = b"spam"
DEF TWO = TUPLE[1]
DEF FIVE = TWO + 3
DEF TRUE  = TRUE_FALSE[0]
DEF FALSE = TRUE_FALSE[1]
DEF INT_TUPLE1 = TUPLE[:2]
DEF INT_TUPLE2 = TUPLE[1:4:2]
DEF ELLIPSIS = ...
DEF EXPRESSION = int(float(2*2)) + int(str(2)) + int(max(1,2,3)) + sum([TWO, FIVE])


def c():
    """
    >>> c()
    120
    """
    cdef char c = CHAR
    return c

def i0():
    """
    >>> i0() == -1
    True
    """
    cdef int i = INT0
    return i

def i1():
    """
    >>> i1() == 42
    True
    """
    cdef int i = INT1
    return i

def i2():
    """
    >>> i2() == 0x42
    True
    """
    cdef int i = INT2
    return i

def i3():
    """
    >>> i3() == -0x42
    True
    """
    cdef int i = INT3
    return i

def l():
    """
    >>> l()
    666
    """
    cdef long l = LONG
    return l

def f():
    """
    >>> f()
    12.5
    """
    cdef float f = FLOAT
    return f

def s():
    """
    see module docstring above
    """
    cdef char* s = STR
    return s

@cython.test_assert_path_exists('//TupleNode')
def constant_tuple():
    """
    >>> constant_tuple()[:-1]
    (1, 2)
    >>> print(constant_tuple()[-1])
    buckle my shoe
    """
    cdef object t = TUPLE
    return t

@cython.test_assert_path_exists('//IntNode')
def tuple_indexing():
    """
    >>> tuple_indexing()
    2
    """
    cdef int two = INT_TUPLE1[-1]
    return two

def two():
    """
    >>> two()
    2
    """
    cdef int two = TWO
    return two

def five():
    """
    >>> five()
    5
    """
    cdef int five = FIVE
    return five

@cython.test_assert_path_exists('//BoolNode')
def true():
    """
    >>> true()
    True
    """
    cdef bint true = TRUE
    return true

@cython.test_assert_path_exists('//BoolNode')
def false():
    """
    >>> false()
    False
    """
    cdef bint false = FALSE
    return false

def ellipsis():
    """
    >>> ellipsis()
    Ellipsis
    """
    return ELLIPSIS

@cython.test_assert_path_exists('//IntNode')
@cython.test_fail_if_path_exists('//AddNode')
def expression():
    """
    >>> expression()
    16
    """
    cdef int i = EXPRESSION
    return i

def none():
    """
    >>> none()
    """
    return NONE
