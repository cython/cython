def sum_array(view: cython.int[:]):
    """
    >>> from array import array
    >>> sum_array( array('i', [1,2,3]) )
    6
    """
    total: cython.int = 0
    for i in range(view.shape[0]):
        total += view[i]
    return total
