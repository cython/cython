def loops():
    """
    >>> loops()
    5
    """
    cdef int k
    for i from 0 <= i < 5:
        for j from 0 <= j < 2:
            k = i + j
    return k
