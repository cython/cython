# mode: run
# tag: cpp, werror

extern from "cpp_namespaces_helper.h" namespace "A":
    ctypedef i32 A_t
    struct S:
        f64 x
        A_t k
    fn A_t A_func(A_t first, A_t)
    fn void f(A_t)

extern from "cpp_namespaces_helper.h" namespace "outer":
    i32 outer_value

extern from "cpp_namespaces_helper.h" namespace "outer::inner":
    i32 inner_value

def test_function(x, y):
    """
    >>> test_function(1, 2)
    3
    >>> test_function(9, 16)
    25
    """
    return A_func(x, y)

def test_nested():
    """
    >>> test_nested()
    10
    100
    """
    print outer_value
    print inner_value

def test_typedef(A_t a):
    """
    >>> test_typedef(3)
    3
    """
    return a

def test_convert_struct(S s):
    """
    >>> py_value = {'x': 3.5, 'k': 10}
    >>> test_convert_struct(py_value) == py_value
    True
    """
    return s
