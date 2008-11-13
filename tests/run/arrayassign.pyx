__doc__ = u"""
>>> test_literal_list_slice_all()
(1, 2, 3, 4, 5)
>>> test_literal_list_slice_start()
(1, 2, 3, 4, 5)
>>> test_literal_list_slice_end()
(1, 2, 3, 4, 5)
>>> test_literal_list_slice_start_end()
(1, 2, 3, 4, 5)

>>> test_literal_list_slice_start_param(2)
(1, 2, 3, 4, 5)
>>> test_literal_list_slice_end_param(4)
(1, 2, 3, 4, 5)
>>> test_literal_list_slice_start_end_param(2,7)
(1, 2, 3, 4, 5)

>>> test_ptr_literal_list_slice_all()
(1, 2, 3, 4, 5)
>>> test_ptr_literal_list_slice_start()
(1, 2, 3, 4, 5)
>>> test_ptr_literal_list_slice_end()
(1, 2, 3, 4, 5)
"""

# this doesn't work - it would reassign the array address!
#
#def test_literal_list():
#    cdef int a[5]
#    a = [1,2,3,4,5]
#    return (a[0], a[1], a[2], a[3], a[4])

def test_literal_list_slice_all():
    cdef int a[5] # = [5,4,3,2,1]
    a[:] = [1,2,3,4,5]
    return (a[0], a[1], a[2], a[3], a[4])

def test_literal_list_slice_start():
    cdef int a[7] # = [7,6,5,4,3,2,1]
    a[2:] = [1,2,3,4,5]
    return (a[2], a[3], a[4], a[5], a[6])

def test_literal_list_slice_end():
    cdef int a[7] # = [7,6,5,4,3,2,1]
    a[:5] = [1,2,3,4,5]
    return (a[0], a[1], a[2], a[3], a[4])

def test_literal_list_slice_start_end():
    cdef int a[9] # = [9,8,7,6,5,4,3,2,1]
    a[2:7] = [1,2,3,4,5]
    return (a[2], a[3], a[4], a[5], a[6])

def test_literal_list_slice_start_param(s):
    cdef int a[9] # = [9,8,7,6,5,4,3,2,1]
    a[s:] = [1,2,3,4,5]
    return (a[2], a[3], a[4], a[5], a[6])
#    return a[s:]

def test_literal_list_slice_end_param(e):
    cdef int a[9] # = [9,8,7,6,5,4,3,2,1]
    a[:e] = [1,2,3,4,5]
    return (a[0], a[1], a[2], a[3], a[4])
#    return a[:e]

def test_literal_list_slice_start_end_param(s,e):
    cdef int a[9] # = [9,8,7,6,5,4,3,2,1]
    a[s:e] = [1,2,3,4,5]
    return (a[2], a[3], a[4], a[5], a[6])
#    return a[s:e]

def test_ptr_literal_list_slice_all():
    cdef int *a = [6,5,4,3,2]
    a[:] = [1,2,3,4,5]
    return (a[0], a[1], a[2], a[3], a[4])

def test_ptr_literal_list_slice_start():
    cdef int *a = [6,5,4,3,2,1]
    a[1:] = [1,2,3,4,5]
    return (a[1], a[2], a[3], a[4], a[5])

def test_ptr_literal_list_slice_end():
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
