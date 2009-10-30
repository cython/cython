cdef union Spam:
    int i
    char c
    float *p[42]

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
