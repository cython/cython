def smoketest():
    """
    >>> smoketest()
    [0, 4, 8]
    """
    print [x*2 for x in range(5) if x % 2 == 0]

def int_runvar():
    """
    >>> int_runvar()
    [0, 4, 8]
    """
    cdef int x
    print [x*2 for x in range(5) if x % 2 == 0]

cdef class A:
    def __repr__(self): return u"A"

def typed():
    """
    >>> typed()
    [A, A, A]
    """
    cdef A obj
    print [obj for obj in [A(), A(), A()]]

def iterdict():
    """
    >>> iterdict()
    [1, 2, 3]
    """
    cdef dict d = dict(a=1,b=2,c=3)
    l = [d[key] for key in d]
    l.sort()
    print l
