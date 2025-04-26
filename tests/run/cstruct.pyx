# mode: run
#tag: struct

cdef struct Grail


cdef struct Spam:
    int i
    char c
    float *p[42]
    Grail *g


cdef struct Grail:
    Spam *s


cdef struct ReservedNames:
    int new
    int case
    int do


cdef Spam spam, ham

cdef void eggs_i(Spam s):
    cdef int j
    j = s.i
    s.i = j

cdef void eggs_c(Spam s):
    cdef char c
    c = s.c
    s.c = c

cdef void eggs_p(Spam s):
    cdef float *p
    p = s.p[0]
    s.p[0] = p

cdef void eggs_g(Spam s):
    cdef float *p
    p = s.p[0]
    s.p[0] = p

spam = ham

def test_i():
    """
    >>> test_i()
    """
    spam.i = 1
    eggs_i(spam)

def test_c():
    """
    >>> test_c()
    """
    spam.c = c'a'
    eggs_c(spam)

def test_p():
    """
    >>> test_p()
    """
    cdef float f
    spam.p[0] = &f
    eggs_p(spam)

def test_g():
    """
    >>> test_g()
    """
    cdef Grail l
    spam.g = &l
    eggs_g(spam)


cdef struct Ints:
    int a, b

def assign_fields_in_loop():
    """
    >>> assign_fields_in_loop()
    2
    """
    cdef int i = 0
    cdef Ints s
    for s.a, s.b in enumerate(range(3)):
        assert s.a == s.b
        assert s.a == i
        i += 1

    assert s.a == s.b
    return s.b


def reserved_names():
    """
    >>> reserved_names()
    (2, 5, 9)
    """
    cdef ReservedNames s1 = ReservedNames(new=2, case=5, do=9)
    cdef ReservedNames s2
    s2.new = s1.new
    s2.case, s2.do = s1.case, s1.do
    return (s2.new, s2.case, s2.do)
