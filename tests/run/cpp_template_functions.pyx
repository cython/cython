# tag: cpp

from libcpp.pair cimport pair

cdef extern from "cpp_template_functions_helper.h":
    cdef T no_arg[T]()
    cdef T one_param[T](T)
    cdef pair[T, U] two_params[T, U](T, U)
    cdef cppclass A[T]:
        pair[T, U] method[U](T, U)
    cdef T nested_deduction[T](const T*)
    pair[T, U] pair_arg[T, U](pair[T, U] a)

def test_no_arg():
    """
    >>> test_no_arg()
    0
    """
    return no_arg[int]()

def test_one_param(int x):
    """
    >>> test_one_param(3)
    (3, 3.0)
    """
    return one_param[int](x), one_param[double](x)

def test_two_params(int x, int y):
    """
    >>> test_two_params(1, 2)
    (1, 2.0)
    """
    return two_params[int, double](x, y)

def test_method(int x, int y):
    """
    >>> test_method(5, 10)
    ((5, 10.0), (5.0, 10))
    """
    cdef A[int] a_int
    cdef A[double] a_double
    return a_int.method[float](x, y), a_double.method[int](x, y)
#    return a_int.method[double](x, y), a_double.method[int](x, y)

def test_simple_deduction(int x, double y):
    """
    >>> test_simple_deduction(1, 2)
    (1, 2.0)
    """
    return one_param(x), one_param(y)

def test_more_deductions(int x, double y):
    """
    >>> test_more_deductions(1, 2)
    (1, 2.0)
    """
    return nested_deduction(&x), nested_deduction(&y)

def test_class_deductions(pair[long, double] x):
    """
    >>> test_class_deductions((1, 1.5))
    (1, 1.5)
    """
    return pair_arg(x)

