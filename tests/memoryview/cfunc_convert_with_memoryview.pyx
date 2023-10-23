# mode: run
# tag: autowrap
# cython: always_allow_keywords=true

fn void memoryview_func_a(f64[:] x):
    x[0] = 1

fn void memoryview_func_b(f64[::1] x):
    x[0] = 2

fn void memoryview_func_c(i32[:] x):
    x[0] = 1

fn void memoryview_func_d(i32[:] x):
    x[0] = 2

fn void memoryview_func_e(i32[:, ::1] x):
    x[0, 0] = 4

fn void memoryview_func_f(i32[::1, :] x):
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
    let a = memoryview_func_a
    let b = memoryview_func_b
    let c = memoryview_func_c
    let d = memoryview_func_d
    let e = memoryview_func_e
    let f = memoryview_func_f
    let f64[1] double_arr = [0]
    let i32[1] int_arr = [0]

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
