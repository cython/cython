# mode: run
# tag: autowrap
# cython: always_allow_keywords=True

cdef void memoryview_func_a(double [:] x):
    x[0] = 1

cdef void memoryview_func_b(double [::1] x):
    x[0] = 2

cdef void memoryview_func_c(int [:] x):
    x[0] = 1

cdef void memoryview_func_d(int [:] x):
    x[0] = 2

cdef void memoryview_func_e(int [:,::1] x):
    x[0,0] = 4

cdef void memoryview_func_f(int [::1,:] x):
    x[0,0] = 4


def test_memview_wrapping():
    """
    We're mainly concerned that the code compiles without the names clashing
    >>> test_memview_wrapping()
    1.0
    2.0
    1
    2
    """
    cdef a = memoryview_func_a
    cdef b = memoryview_func_b
    cdef c = memoryview_func_c
    cdef d = memoryview_func_d
    cdef e = memoryview_func_e
    cdef f = memoryview_func_f
    cdef double[1] double_arr = [0]
    cdef int[1] int_arr = [0]

    a(<double[:1]> double_arr)
    print(double_arr[0])
    b(<double[:1:1]> double_arr)
    print(double_arr[0])
    c(<int[:1]> int_arr)
    print(int_arr[0])
    d(<int[:1:1]> int_arr)
    print(int_arr[0])
    # don't call e and f because it's harder without needing extra dependencies
    # it's mostly a compile test for them
