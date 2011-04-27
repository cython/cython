# mode: run

cimport cython
from cpython cimport Py_INCREF

from Cython import Shadow as pure_cython

ctypedef char * string_t

ctypedef cython.fused_type(int, long, float, double, string_t) fused_type1
ctypedef cython.fused_type(string_t) fused_type2


def test_pure():
    """
    >>> test_pure()
    (10+0j)
    """
    mytype = pure_cython.typedef(pure_cython.fused_type(int, long, complex))
    print mytype(10)


cdef cdef_func_with_fused_args(fused_type1 x, fused_type1 y, fused_type2 z):
    print x, y, z
    return x + y

def test_cdef_func_with_fused_args():
    """
    >>> test_cdef_func_with_fused_args()
    spam ham eggs
    spamham
    10 20 butter
    30
    4.2 8.6 bunny
    12.8
    """
    print cdef_func_with_fused_args('spam', 'ham', 'eggs')
    print cdef_func_with_fused_args(10, 20, 'butter')
    print cdef_func_with_fused_args(4.2, 8.6, 'bunny')

cdef fused_type1 fused_with_pointer(fused_type1 *array):
    for i in range(5):
        print array[i]

    obj = array[0] + array[1] + array[2] + array[3] + array[4]
    # if cython.typeof(fused_type1) is string_t:
    Py_INCREF(obj)
    return obj

def test_fused_with_pointer():
    """
    >>> test_fused_with_pointer()
    0
    1
    2
    3
    4
    10
    <BLANKLINE>
    0
    1
    2
    3
    4
    10
    <BLANKLINE>
    0.0
    1.0
    2.0
    3.0
    4.0
    10.0
    <BLANKLINE>
    humpty
    dumpty
    fall
    splatch
    breakfast
    humptydumptyfallsplatchbreakfast
    """
    cdef int int_array[5]
    cdef long long_array[5]
    cdef float float_array[5]
    cdef string_t string_array[5]

    cdef char *s1 = "humpty", *s2 = "dumpty", *s3 = "fall", *s4 = "splatch", *s5 = "breakfast"

    strings = ["humpty", "dumpty", "fall", "splatch", "breakfast"]

    for i in range(5):
        int_array[i] = i
        long_array[i] = i
        float_array[i] = i
        s = strings[i]
        string_array[i] = s

    print fused_with_pointer(int_array)
    print
    print fused_with_pointer(long_array)
    print
    print fused_with_pointer(float_array)
    print
    print fused_with_pointer(string_array)
