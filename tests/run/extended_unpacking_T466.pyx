# extension to T409

def simple_parallel_typed():
    """
    >>> simple_parallel_typed()
    (1, 2, [1, 2], [1, 2])
    """
    cdef int a,c
    a, c = d = e = [1,2]
    return a, c, d, e

def simple_parallel_int_mix():
    """
    >>> simple_parallel_int_mix()
    (1, 2, 1, 2, 1, 2, [1, 2], [1, 2])
    """
    cdef int ai,bi
    cdef long al,bl
    cdef object ao, bo
    ai, bi = al, bl = ao, bo = c = d = [1,2]
    return ao, bo, ai, bi, al, bl, c, d
