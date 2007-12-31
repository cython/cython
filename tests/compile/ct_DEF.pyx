DEF CHAR = c'x'
DEF INT = 42
DEF LONG = 666L
DEF FLOAT = 17.88
DEF STR = "spam"
DEF TUPLE = (1, 2, "buckle my shoe")
DEF TWO = TUPLE[1]
DEF FIVE = TWO + 3

cdef void f():
    cdef char c
    cdef int i
    cdef long l
    cdef float f
    cdef char *s
    cdef int two
    cdef int five
    c = CHAR
    i = INT
    l = LONG
    f = FLOAT
    s = STR
    two = TWO
    five = FIVE
    