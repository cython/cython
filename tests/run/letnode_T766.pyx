# mode: run
# ticket: 766
# tag: letnode

def test_letnode_range(int n):
    """
    >>> [i() for i in test_letnode_range(5)]
    [0, 1, 2, 3, 4]
    """
    ret = []
    for i in range(n):
        def bar(x=i):
            return x
        ret.append(bar)
    return ret

def test_letnode_enumerate(a):
    """
    >>> [i() for i in test_letnode_enumerate("abc")]
    [0, 1, 2]
    """
    cdef int n
    ret = []
    for n, i in enumerate(a):
        def bar(x=n):
            return x
        ret.append(bar)
    return ret
