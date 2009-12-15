__doc__ = u"""
    >>> c()
    120
    >>> i0() == -1
    True
    >>> i1() == 42
    True
    >>> i2() == 0x42
    True
    >>> i3() == -0x42
    True
    >>> l()
    666
    >>> f()
    12.5
    >>> s()
    b'spam'
    >>> two()
    2
    >>> five()
    5
    >>> true()
    True
    >>> false()
    False
"""

import sys
if sys.version_info[0] < 3:
    __doc__ = __doc__.replace(u" b'", u" '")
else:
    __doc__ = __doc__.replace(u" 042", u" 0o42")

DEF TUPLE = (1, 2, u"buckle my shoe")
DEF TRUE_FALSE = (True, False)

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

def c():
    cdef char c
    c = CHAR
    return c

def i0():
    cdef int i
    i = INT0
    return i

def i1():
    cdef int i
    i = INT1
    return i

def i2():
    cdef int i
    i = INT2
    return i

def i3():
    cdef int i
    i = INT3
    return i

def l():
    cdef long l
    l = LONG
    return l

def f():
    cdef float f
    f = FLOAT
    return f

def s():
    cdef char *s
    s = STR
    return s

# this does not work!
#def t():
#    cdef object t
#    t = TUPLE
#    return t

def two():
    cdef int two
    two = TWO
    return two

# this doesn't currently work!
#def two2():
#    cdef int two
#    two = INT_TUPLE1[-1]
#    return two

def five():
    cdef int five
    five = FIVE
    return five

def true():
    cdef bint true
    true = TRUE
    return true

def false():
    cdef bint false
    false = FALSE
    return false
