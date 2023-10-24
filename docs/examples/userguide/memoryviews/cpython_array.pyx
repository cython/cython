def sum_array(i32[:] view):
    """
    >>> from array import array
    >>> sum_array(array('i', [1, 2, 3]))
    6
    """
    let i32 total = 0
    for i in range(view.shape[0]):
        total += view[i]
    return total
