def f(dict d):
    """
    >>> f({1:1, 2:2})
    [1, 2]
    """
    cdef dict d_new = {}
    l = []
    for k in d:
        d = d_new
        l.append(k)
    l.sort()
    return l
