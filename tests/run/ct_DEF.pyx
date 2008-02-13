__doc__ = """
    >>> c()
    120
    >>> i()
    42
    >>> l()
    666
    >>> f()
    12.5
    >>> s()
    'spam'
    >>> two()
    2
    >>> five()
    5
    >>> true()
    True
    >>> false()
    False
"""

DEF TUPLE = (1, 2, "buckle my shoe")
DEF TRUE_FALSE = (True, False)

DEF CHAR = c'x'
DEF INT = 42
DEF LONG = 666L
DEF FLOAT = 12.5
DEF STR = "spam"
DEF TWO = TUPLE[1]
DEF FIVE = TWO + 3
DEF TRUE  = TRUE_FALSE[0]
DEF FALSE = TRUE_FALSE[1]

def c():
    cdef char c
    c = CHAR
    return c

def i():
    cdef int i
    i = INT
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
