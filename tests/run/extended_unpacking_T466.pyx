# extension to T409

def simple_parallel_typed():
    """
    >>> simple_parallel_typed()
    (1, 2, [1, 2], [1, 2])
    """
    cdef int a,c
    a, c = d = e = [1,2]
    return a, c, d, e
