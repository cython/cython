# mode: run

cimport cython

def test_literal_list():
    """
    >>> test_literal_list()
    (1, 2, 3, 4, 5)
    """
    cdef int a[5]
    a = [1,2,3,4,5]
    return (a[0], a[1], a[2], a[3], a[4])

def test_literal_list_multiplied():
    """
    >>> test_literal_list_multiplied()
    (1, 2, 1, 2, 1, 2)
    """
    cdef int a[6]
    a = [1,2] * 3
    return (a[0], a[1], a[2], a[3], a[4], a[5])

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


@cython.test_assert_path_exists(
    '//ReturnStatNode//CoerceToPyTypeNode'
)
def test_starred_from_array():
    """
    >>> test_starred_from_array()
    (1, [2, 3, 4], 5)
    """
    cdef int[5] a
    a[0] = 1
    a[1] = 2
    a[2] = 3
    a[3] = 4
    a[4] = 5
    x, *y, z = a
    return x, y, z


@cython.test_fail_if_path_exists(
    '//ParallelAssignmentNode//CoerceToPyTypeNode',
    '//ParallelAssignmentNode//CoerceFromPyTypeNode',
)
@cython.test_assert_path_exists(
    '//ParallelAssignmentNode',
    '//ReturnStatNode//CoerceToPyTypeNode'
)
def test_multiple_from_array():
    """
    >>> test_multiple_from_array()
    (1, 2, 3)
    """
    cdef int[3] a
    a[0] = 1
    a[1] = 2
    a[2] = 3
    x, y, z = a
    return x, y, z


@cython.test_fail_if_path_exists(
    '//ParallelAssignmentNode//CoerceToPyTypeNode'
)
@cython.test_assert_path_exists(
    '//ParallelAssignmentNode',
    '//ReturnStatNode//CoerceToPyTypeNode'
)
def test_multiple_from_array_full_slice():
    """
    >>> test_multiple_from_array_full_slice()
    (1, 2, 3)
    """
    cdef int[3] a
    a[0] = 1
    a[1] = 2
    a[2] = 3
    x, y, z = a[:]
    return x, y, z


@cython.test_fail_if_path_exists(
    '//ParallelAssignmentNode//CoerceToPyTypeNode'
)
@cython.test_assert_path_exists(
    '//ParallelAssignmentNode',
    '//ReturnStatNode//CoerceToPyTypeNode'
)
def test_multiple_from_slice():
    """
    >>> test_multiple_from_slice()
    (5, 4, 3)
    """
    cdef int *a = [6,5,4,3,2,1]
    x, y, z = a[1:4]
    return x, y, z


def test_slice_from_multiple():
    """
    >>> test_slice_from_multiple()
    (6, -1, -2, -3, 2, 1)
    """
    cdef int *a = [6,5,4,3,2,1]
    a[1:4] = -1, -2, -3
    return a[0], a[1], a[2], a[3], a[4], a[5]

def test_literal_tuple():
    """
    >>> test_literal_tuple()
    (1, 2, 3, 4, 5)
    """
    cdef int a[5]
    a = (1,2,3,4,5)
    return (a[0], a[1], a[2], a[3], a[4])

def test_list(list l):
    """
    >>> test_list([1, 2, 3, 4, 5])
    (1, 2, 3, 4, 5)
    """
    cdef int a[5]
    a[:] = l
    return (a[0], a[1], a[2], a[3], a[4])


def assign_all_from_pointer():
    """
    >>> assign_all_from_pointer()
    (1, 2, 3, 4, 5)
    """
    cdef int *v = [1, 2, 3, 4, 5]
    cdef int[5] a
    a = v
    return (a[0], a[1], a[2], a[3], a[4])


def assign_full_from_pointer():
    """
    >>> assign_full_from_pointer()
    (1, 2, 3, 4, 5)
    """
    cdef int *v = [1, 2, 3, 4, 5]
    cdef int[5] a
    a[:] = v
    return (a[0], a[1], a[2], a[3], a[4])


def assign_slice_end_from_pointer():
    """
    >>> assign_slice_end_from_pointer()
    (1, 2, 3, 4, 123)
    """
    cdef int *v = [1, 2, 3, 4, 5]
    cdef int[5] a
    a[4] = 123
    a[:4] = v
    return (a[0], a[1], a[2], a[3], a[4])


def assign_slice_start_from_pointer():
    """
    >>> assign_slice_start_from_pointer()
    (123, 234, 1, 2, 3)
    """
    cdef int *v = [1, 2, 3, 4, 5]
    cdef int[5] a
    a[0] = 123
    a[1] = 234
    a[2:] = v
    return (a[0], a[1], a[2], a[3], a[4])


def assign_slice_start_end_from_pointer():
    """
    >>> assign_slice_start_end_from_pointer()
    (123, 234, 1, 2, 345)
    """
    cdef int *v = [1, 2, 3, 4, 5]
    cdef int[5] a
    a[0] = 123
    a[1] = 234
    a[4] = 345
    a[2:4] = v
    return (a[0], a[1], a[2], a[3], a[4])


'''
# FIXME: make this work:
def assign_slice_start_end_from_sliced_pointer():
    """
    >>> assign_slice_start_end_from_sliced_pointer()
    (123, 234, 3, 4, 345)
    """
    cdef int *v = [1, 2, 3, 4, 5]
    cdef int[5] a
    a[0] = 123
    a[1] = 234
    a[4] = 345
    a[2:4] = v[2:4]
    return (a[0], a[1], a[2], a[3], a[4])


def assign_from_longer_array_slice():
    """
    >>> assign_from_longer_array_slice()
    [3, 4, 5]
    """
    cdef int[5] a
    cdef int[3] b
    a[0] = 1
    a[1] = 2
    a[2] = 3
    a[3] = 4
    a[4] = 5
    b[0] = 11
    b[1] = 12
    b[2] = 13
    b = a[2:]
    return b
'''


def assign_slice_from_shorter_array():
    """
    >>> assign_slice_from_shorter_array()
    [1, 11, 12, 13, 5]
    """
    cdef int[5] a
    cdef int[3] b
    a[0] = 1
    a[1] = 2
    a[2] = 3
    a[3] = 4
    a[4] = 5
    b[0] = 11
    b[1] = 12
    b[2] = 13
    a[1:4] = b
    return a


cdef enum:
    SIZE = 2

ctypedef int[SIZE] int_array_dyn


def assign_ptr_to_unknown_csize():
    """
    >>> assign_ptr_to_unknown_csize()
    [1, 2]
    """
    cdef int* v = [1, 2, 3, 4, 5]
    cdef int_array_dyn d
    d = v
    return d


def assign_to_wrong_csize():
    """
    >>> assign_to_wrong_csize()
    Traceback (most recent call last):
    ValueError: Assignment to slice of wrong length, expected 3, got 2
    """
    cdef int_array_dyn d
    cdef int v[3]
    v[0] = 1
    v[1] = 2
    v[2] = 3
    d = v
    return d


def assign_full_array_slice_to_array():
    """
    >>> assign_full_array_slice_to_array()
    [1, 2, 3]
    """
    cdef int[3] x, y
    x[0] = 1
    x[1] = 2
    x[2] = 3
    y = x[:]
    return y


cdef class ArrayOwner:
    cdef readonly int[3] array

    def __init__(self, a, b, c):
        self.array = (a, b, c)


def assign_from_array_attribute():
    """
    >>> assign_from_array_attribute()
    [1, 2, 3]
    """
    cdef int[3] v
    a = ArrayOwner(1, 2, 3)
    v = a.array[:]
    return v
