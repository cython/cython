# mode: run
# tag: cpp, warnings

cimport cython
from libcpp.pair cimport pair
from libcpp.vector cimport vector

cdef extern from "cpp_template_functions_helper.h":
    cdef T no_arg[T]()
    cdef T one_param[T](T)
    cdef pair[T, U] two_params[T, U](T, U)
    cdef cppclass A[T]:
        pair[T, U] method[U](T, U)
        U part_method[U](pair[T, U])
        U part_method_ref[U](pair[T, U]&)
        int overloaded(double x)
        T overloaded(pair[T, T])
        U overloaded[U](vector[U])
        X overloaded[X](char* s, vector[X])
    cdef T nested_deduction[T](const T*)
    pair[T, U] pair_arg[T, U](pair[T, U] a)
    cdef T* pointer_param[T](T*)
    cdef cppclass double_pair(pair[double, double]):
        double_pair(double, double)

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
    ((5, 10.0), (5.0, 10), (5, 10), (5.0, 10))
    """
    cdef A[int] a_int
    cdef A[double] a_double
    return (a_int.method[float](x, y), a_double.method[int](x, y),
        a_int.method(x, y), a_double.method(x, y))
#    return a_int.method[double](x, y), a_double.method[int](x, y)

def test_part_method(int x, int y):
    """
    >>> test_part_method(5, 10)
    (10.0, 10, 10.0)
    """
    cdef A[int] a_int
    cdef pair[int, double] p_int = (x, y)
    cdef A[double] a_double
    cdef pair[double, int] p_double = (x, y)
    return (a_int.part_method(p_int),
        a_double.part_method(p_double),
        a_double.part_method_ref(double_pair(x, y)))

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

def test_deduce_through_pointers(int k):
    """
    >>> test_deduce_through_pointers(5)
    (5, 5.0)
    """
    cdef double x = k
    return pointer_param(&k)[0], pointer_param(&x)[0]

def test_inference(int k):
    """
    >>> test_inference(27)
    27
    """
    res = one_param(&k)
    assert cython.typeof(res) == 'int *', cython.typeof(res)
    return res[0]

def test_overload_GH1583():
    """
    >>> test_overload_GH1583()
    """
    cdef A[int] a
    assert a.overloaded(1.5) == 1
    cdef pair[int, int] p = (2, 3)
    assert a.overloaded(p) == 2
    cdef vector[double] v = [0.25, 0.125]
    assert a.overloaded(v) == 0.25
    assert a.overloaded("s", v) == 0.25
    # GH Issue #1584
    # assert a.overloaded[double](v) == 0.25
