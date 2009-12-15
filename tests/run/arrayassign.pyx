# this doesn't work - it would reassign the array address!
#
#def test_literal_list():
#    cdef int a[5]
#    a = [1,2,3,4,5]
#    return (a[0], a[1], a[2], a[3], a[4])

def test_literal_list_slice_all():
    """
    >>> test_literal_list_slice_all()
    (1, 2, 3, 4, 5)
    """
    cdef int a[5] # = [5,4,3,2,1]
    a[:] = [1,2,3,4,5]
    return (a[0], a[1], a[2], a[3], a[4])

def test_literal_list_slice_start():
    """
    >>> test_literal_list_slice_start()
    (1, 2, 3, 4, 5)
    """
    cdef int a[7] # = [7,6,5,4,3,2,1]
    a[2:] = [1,2,3,4,5]
    return (a[2], a[3], a[4], a[5], a[6])

def test_literal_list_slice_end():
    """
    >>> test_literal_list_slice_end()
    (1, 2, 3, 4, 5)
    """
    cdef int a[7] # = [7,6,5,4,3,2,1]
    a[:5] = [1,2,3,4,5]
    return (a[0], a[1], a[2], a[3], a[4])

def test_literal_list_slice_start_end():
    """
    >>> test_literal_list_slice_start_end()
    (1, 2, 3, 4, 5)
    """
    cdef int a[9] # = [9,8,7,6,5,4,3,2,1]
    a[2:7] = [1,2,3,4,5]
    return (a[2], a[3], a[4], a[5], a[6])

def test_literal_list_slice_start_param(s):
    """
    >>> test_literal_list_slice_start_param(4)
    (1, 2, 3, 4, 5)
    >>> test_literal_list_slice_start_param(3)
    Traceback (most recent call last):
    ValueError: Assignment to slice of wrong length, expected 5, got 6
    >>> test_literal_list_slice_start_param(5)
    Traceback (most recent call last):
    ValueError: Assignment to slice of wrong length, expected 5, got 4
    """
    cdef int a[9] # = [9,8,7,6,5,4,3,2,1]
    a[s:] = [1,2,3,4,5]
    return (a[4], a[5], a[6], a[7], a[8])
#    return a[s:]

def test_literal_list_slice_end_param(e):
    """
    >>> test_literal_list_slice_end_param(5)
    (1, 2, 3, 4, 5)
    >>> test_literal_list_slice_end_param(4)
    Traceback (most recent call last):
    ValueError: Assignment to slice of wrong length, expected 5, got 4
    >>> test_literal_list_slice_end_param(6)
    Traceback (most recent call last):
    ValueError: Assignment to slice of wrong length, expected 5, got 6
    """
    cdef int a[9] # = [9,8,7,6,5,4,3,2,1]
    a[:e] = [1,2,3,4,5]
    return (a[0], a[1], a[2], a[3], a[4])
#    return a[:e]

def test_literal_list_slice_start_end_param(s,e):
    """
    >>> test_literal_list_slice_start_end_param(2,7)
    (1, 2, 3, 4, 5)
    >>> test_literal_list_slice_start_end_param(3,7)
    Traceback (most recent call last):
    ValueError: Assignment to slice of wrong length, expected 5, got 4
    >>> test_literal_list_slice_start_end_param(1,7)
    Traceback (most recent call last):
    ValueError: Assignment to slice of wrong length, expected 5, got 6
    >>> test_literal_list_slice_start_end_param(2,6)
    Traceback (most recent call last):
    ValueError: Assignment to slice of wrong length, expected 5, got 4
    >>> test_literal_list_slice_start_end_param(2,8)
    Traceback (most recent call last):
    ValueError: Assignment to slice of wrong length, expected 5, got 6
    >>> test_literal_list_slice_start_end_param(3,6)
    Traceback (most recent call last):
    ValueError: Assignment to slice of wrong length, expected 5, got 3
    >>> test_literal_list_slice_start_end_param(1,8)
    Traceback (most recent call last):
    ValueError: Assignment to slice of wrong length, expected 5, got 7
    """
    cdef int a[9] # = [9,8,7,6,5,4,3,2,1]
    a[s:e] = [1,2,3,4,5]
    return (a[2], a[3], a[4], a[5], a[6])
#    return a[s:e]

def test_ptr_literal_list_slice_all():
    """
    >>> test_ptr_literal_list_slice_all()
    (1, 2, 3, 4, 5)
    """
    cdef int *a = [6,5,4,3,2]
    a[:] = [1,2,3,4,5]
    return (a[0], a[1], a[2], a[3], a[4])

def test_ptr_literal_list_slice_start():
    """
    >>> test_ptr_literal_list_slice_start()
    (1, 2, 3, 4, 5)
    """
    cdef int *a = [6,5,4,3,2,1]
    a[1:] = [1,2,3,4,5]
    return (a[1], a[2], a[3], a[4], a[5])

def test_ptr_literal_list_slice_end():
    """
    >>> test_ptr_literal_list_slice_end()
    (1, 2, 3, 4, 5)
    """
    cdef int *a = [6,5,4,3,2,1]
    a[:5] = [1,2,3,4,5]
    return (a[0], a[1], a[2], a[3], a[4])

# tuples aren't supported (yet)
#
#def test_literal_tuple():
#    cdef int a[5]
#    a = (1,2,3,4,5)
#    return (a[0], a[1], a[2], a[3], a[4])

# this would be nice to have:
#
#def test_list(list l):
#    cdef int a[5]
#    a[:] = l
#    return (a[0], a[1], a[2], a[3], a[4])
