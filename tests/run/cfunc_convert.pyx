# mode: run
# cython: always_allow_keywords=True

cimport cython

from libc.math cimport sqrt

cdef void empty_cfunc():
    print "here"

# same signature
cdef void another_empty_cfunc():
    print "there"

def call_empty_cfunc():
    """
    >>> call_empty_cfunc()
    here
    there
    """
    cdef object py_func = empty_cfunc
    py_func()
    cdef object another_py_func = another_empty_cfunc
    another_py_func()


cdef double square_c(double x):
    return x * x

def call_square_c(x):
    """
    >>> call_square_c(2)
    4.0
    >>> call_square_c(-7)
    49.0
    """
    cdef object py_func = square_c
    return py_func(x)


def return_square_c():
    """
    >>> square_c = return_square_c()
    >>> square_c(5)
    25.0
    >>> square_c(x=4)
    16.0
    >>> square_c.__doc__   # FIXME: try to make original C function name available
    'wrap(x: float) -> float'
    """
    return square_c


def return_libc_sqrt():
    """
    >>> sqrt = return_libc_sqrt()
    >>> sqrt(9)
    3.0
    >>> sqrt(x=9)
    3.0
    >>> sqrt.__doc__
    'wrap(x: float) -> float'
    """
    return sqrt


global_csqrt = sqrt

def test_global():
    """
    >>> global_csqrt(9)
    3.0
    >>> global_csqrt.__doc__
    'wrap(x: float) -> float'
    >>> test_global()
    double (double) nogil
    Python object
    """
    print cython.typeof(sqrt)
    print cython.typeof(global_csqrt)


cdef long long rad(long long x):
    cdef long long rad = 1
    for p in range(2, <long long>sqrt(x) + 1):
        if x % p == 0:
            rad *= p
            while x % p == 0:
                x //= p
        if x == 1:
            break
    return rad

cdef bint abc(long long a, long long b, long long c) except -1:
    if a + b != c:
        raise ValueError("Not a valid abc candidate: (%s, %s, %s)" % (a, b, c))
    return rad(a*b*c) < c

def call_abc(a, b, c):
    """
    >>> call_abc(2, 3, 5)
    False
    >>> call_abc(1, 63, 64)
    True
    >>> call_abc(2, 3**10 * 109, 23**5)
    True
    >>> call_abc(a=2, b=3**10 * 109, c=23**5)
    True
    >>> call_abc(1, 1, 1)
    Traceback (most recent call last):
    ...
    ValueError: Not a valid abc candidate: (1, 1, 1)
    """
    cdef object py_func = abc
    return py_func(a, b, c)

def return_abc():
    """
    >>> abc = return_abc()
    >>> abc(2, 3, 5)
    False
    >>> abc.__doc__
    "wrap(a: 'long long', b: 'long long', c: 'long long') -> bool"
    """
    return abc


ctypedef double foo
cdef foo test_typedef_cfunc(foo x):
    return x

def test_typedef(x):
    """
    >>> test_typedef(100)
    100.0
    """
    return (<object>test_typedef_cfunc)(x)


cdef union my_union:
    int a
    double b

cdef struct my_struct:
    int which
    my_union y

cdef my_struct c_struct_builder(int which, int a, double b):
    cdef my_struct value
    value.which = which
    if which:
        value.y.a = a
    else:
        value.y.b = b
    return value

def return_struct_builder():
    """
    >>> make = return_struct_builder()
    >>> d = make(0, 1, 2)
    >>> d['which']
    0
    >>> d['y']['b']
    2.0
    >>> d = make(1, 1, 2)
    >>> d['which']
    1
    >>> d['y']['a']
    1
    >>> make.__doc__
    "wrap(which: 'int', a: 'int', b: float) -> 'my_struct'"
    """
    return c_struct_builder


cdef object test_object_params_cfunc(a, b):
    return a, b

def test_object_params(a, b):
    """
    >>> test_object_params(1, 'a')
    (1, 'a')
    """
    return (<object>test_object_params_cfunc)(a, b)


cdef tuple test_builtin_params_cfunc(list a, dict b):
    return a, b

def test_builtin_params(a, b):
    """
    >>> test_builtin_params([], {})
    ([], {})
    >>> test_builtin_params(1, 2)
    Traceback (most recent call last):
    ...
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    """
    return (<object>test_builtin_params_cfunc)(a, b)

def return_builtin_params_cfunc():
    """
    >>> cfunc = return_builtin_params_cfunc()
    >>> cfunc([1, 2], {'a': 3})
    ([1, 2], {'a': 3})
    >>> cfunc.__doc__
    'wrap(a: list, b: dict) -> tuple'
    """
    return test_builtin_params_cfunc


cdef class A:
    def __repr__(self):
        return self.__class__.__name__

cdef class B(A):
    pass

cdef A test_cdef_class_params_cfunc(A a, B b):
    return b

def test_cdef_class_params(a, b):
    """
    >>> test_cdef_class_params(A(), B())
    B
    >>> test_cdef_class_params(B(), A())
    Traceback (most recent call last):
    ...
    TypeError: Argument 'b' has incorrect type (expected cfunc_convert.B, got cfunc_convert.A)
    """
    return (<object>test_cdef_class_params_cfunc)(a, b)
