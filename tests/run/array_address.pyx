ctypedef int five_ints[5]

def test_array_address(int ix, int x):
    """
    >>> test_array_address(0, 100)
    100
    >>> test_array_address(2, 200)
    200
    """
    cdef five_ints a
    a[:] = [1, 2, 3, 4, 5]
    cdef five_ints *a_ptr = &a
    a_ptr[0][ix] = x
    return a[ix]
