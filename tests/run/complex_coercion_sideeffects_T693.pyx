# mode: run
# ticket: t693

cdef double complex func(double complex x):                                                  
    print "hello"
    return x

def test_coercion():
    """
    >>> c = test_coercion()
    hello
    >>> c.real == 0.5
    True
    >>> c.imag == 1.5
    True
    """
    cdef object x = func(0.5 + 1.5j)
    return x
