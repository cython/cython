cdef int i, j, k
i = 17; j = 42; k = i * j
if j > k: i = 88
else: i = 99; j = k

def result():
    """
    >>> result() == (99, 17*42, 17*42)
    True
    """
    return (i,j,k)
