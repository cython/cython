# ticket: t404

cdef long foo(long x):
    print "foo(%s)" % x
    return x

def test_or(long a, long b):
    """
    >>> test_or(1,2)
    foo(1)
    1
    >>> test_or(1,0)
    foo(1)
    1
    >>> test_or(0,2)
    foo(0)
    foo(2)
    2
    >>> test_or(0,0)
    foo(0)
    foo(0)
    0
    """
    print foo(a) or foo(b)

def test_and(long a, long b):
    """
    >>> test_and(1,2)
    foo(1)
    foo(2)
    2
    >>> test_and(1,0)
    foo(1)
    foo(0)
    0
    >>> test_and(0,2)
    foo(0)
    0
    >>> test_and(0,0)
    foo(0)
    0
    """
    print foo(a) and foo(b)
