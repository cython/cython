cdef long foo(long x):
    print "foo(%s)" % x
    return x

def test_or(long a, long b):
    """
    >>> test_or(1,2)
    foo(1)
    True
    >>> test_or(1,0)
    foo(1)
    True
    >>> test_or(0,2)
    foo(0)
    foo(2)
    True
    >>> test_or(0,0)
    foo(0)
    foo(0)
    False
    """
    print foo(a) or foo(b)

def test_and(long a, long b):
    """
    >>> test_and(1,2)
    foo(1)
    foo(2)
    True
    >>> test_and(1,0)
    foo(1)
    foo(0)
    False
    >>> test_and(0,2)
    foo(0)
    False
    >>> test_and(0,0)
    foo(0)
    False
    """
    print foo(a) and foo(b)
