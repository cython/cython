
cimport cython

__doc__ = u"""
    >>> s()
    b'spam'
"""

_unicode = unicode

import sys
IS_PY3 = sys.version_info[0] >= 3

if not IS_PY3:
    __doc__ = __doc__.replace(u" b'", u" '")


def print_large_number(n):
    print(str(n).rstrip('L'))


DEF TUPLE = (1, 2, u"buckle my shoe")
DEF TRUE_FALSE = (True, False)
DEF NONE = None

DEF CHAR = c'x'
DEF INT0 = -1
DEF INT1 = 42
DEF INT2 = 0x42
DEF INT3 = -0x42
DEF LONG = 666L
DEF LARGE_NUM32 = (1 << 32) - 1
DEF LARGE_NUM64 = (1 << 64) - 1
DEF FLOAT = 12.5
DEF BYTES = b"spam"
DEF UNICODE = u"spam-u"
DEF TWO = TUPLE[1]
DEF FIVE = TWO + 3
DEF TRUE  = TRUE_FALSE[0]
DEF FALSE = TRUE_FALSE[1]
DEF INT_TUPLE1 = TUPLE[:2]
DEF INT_TUPLE2 = TUPLE[1:4:2]
DEF ELLIPSIS = ...
DEF EXPRESSION = int(float(2*2)) + int(str(2)) + int(max(1,2,3)) + sum([TWO, FIVE])
DEF UNICODE_EXPRESSION = unicode(BYTES.decode('utf8')).encode('ascii').decode('latin1')


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

def large_nums():
    """
    >>> ul32, ul64, l64, n64 = large_nums()
    >>> print_large_number(ul32)
    4294967295
    >>> print_large_number(ul64)
    18446744073709551615
    >>> print_large_number(l64)
    4294967295
    >>> print_large_number(n64)
    -4294967295
    """
    cdef unsigned long ul32 = LARGE_NUM32
    cdef unsigned long long ul64 = LARGE_NUM64
    cdef long long l64 = LARGE_NUM32
    cdef long long n64 = -LARGE_NUM32
    return ul32, ul64, l64, n64

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
    cdef char* s = BYTES
    return s

def type_of_bytes():
    """
    >>> t, s = type_of_bytes()
    >>> assert t is bytes, t
    >>> assert type(s) is bytes, type(s)
    """
    t = type(BYTES)
    s = BYTES
    return t, s

def type_of_unicode():
    """
    >>> t, s = type_of_unicode()
    >>> assert t is _unicode, t
    >>> assert type(s) is _unicode, type(s)
    """
    t = type(UNICODE)
    s = UNICODE
    return t, s

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


def unicode_expression():
    """
    >>> print(unicode_expression())
    spam
    """
    s = UNICODE_EXPRESSION
    return s


def none():
    """
    >>> none()
    """
    return NONE
