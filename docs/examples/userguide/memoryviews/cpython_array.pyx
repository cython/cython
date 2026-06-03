def sum_array(int[:] view):
    """
    >>> from array import array
    >>> sum_array( array('i', [1,2,3]) )
    6
    """
    cdef int total = 0
    for i in range(view.shape[0]):
        total += view[i]
    return total
