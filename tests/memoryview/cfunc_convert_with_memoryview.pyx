# mode: run
# tag: autowrap
# cython: always_allow_keywords=true

cdef void memoryview_func_a(f64 [:] x):
    x[0] = 1

cdef void memoryview_func_b(f64 [::1] x):
    x[0] = 2

cdef void memoryview_func_c(i32 [:] x):
    x[0] = 1

cdef void memoryview_func_d(i32 [:] x):
    x[0] = 2

cdef void memoryview_func_e(i32 [:, ::1] x):
    x[0, 0] = 4

cdef void memoryview_func_f(i32 [::1, :] x):
    x[0, 0] = 4

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
    cdef f64[1] double_arr = [0]
    cdef i32[1] int_arr = [0]

    a(<f64[:1]> double_arr)
    print(double_arr[0])
    b(<f64[:1:1]> double_arr)
    print(double_arr[0])
    c(<i32[:1]> int_arr)
    print(int_arr[0])
    d(<i32[:1:1]> int_arr)
    print(int_arr[0])
    # don't call e and f because it's harder without needing extra dependencies
    # it's mostly a compile test for them
