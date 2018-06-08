import cython

def simple_convert(*o):
    """
    >>> simple_convert(1, 2)
    (1, 2.0)

    >>> simple_convert(1)
    Traceback (most recent call last):
    ...
    TypeError: Expected a tuple of size 2, got tuple
    >>> simple_convert(1, 2, 3)
    Traceback (most recent call last):
    ...
    TypeError: Expected a tuple of size 2, got tuple
    """
    cdef (int, double) xy = o
    return xy

def indexing((int, double) xy):
    """
    >>> indexing((1, 2))
    (2, 3.0)
    """
    x = xy[0]
    y = xy[1]
    xy[0] = x + 1
    xy[1] = y + 1
    return xy

def unpacking((int, double) xy):
    """
    >>> unpacking((1, 2))
    (1, 2.0)
    """
    x, y = xy
    return x, y

cdef (int, double) side_effect((int, double) xy):
    print "called with", xy
    return xy

def unpacking_with_side_effect((int, double) xy):
    """
    >>> unpacking_with_side_effect((1, 2))
    called with (1, 2.0)
    (1, 2.0)
    """
    x, y = side_effect(xy)
    return x, y

def packing_tuple(int x, double y):
    """
    >>> packing_tuple(1, 2)
    (1, 2.0)
    """
    cdef (int, double) xy = (x, y)
    assert xy == (x, y), xy
    xy = (x, y) * 1
    assert xy == (x, y), xy
    xy = 1 * (x, y)
    return xy

def packing_list(int x, double y):
    """
    >>> packing_list(1, 2)
    (1, 2.0)
    """
    cdef (int, double) xy = [x, y]
    assert xy == (x, y), xy
    xy = [x, y] * 1
    assert xy == (x, y), xy
    xy = 1 * [x, y]
    return xy

def coerce_packing_tuple(int x, int y):
    cdef (int, double) xy = (x, y)
    """
    >>> coerce_packing_tuple(1, 2)
    (1, 2.0)
    """
    return xy

def c_types(int a, double b):
    """
    >>> c_types(1, 2)
    (1, 2.0)
    """
    cdef int* a_ptr
    cdef double* b_ptr
    cdef (int*, double*) ab = (&a, &b)
    a_ptr, b_ptr = ab
    return a_ptr[0], b_ptr[0]


cdef union Union:
    int x
    double y


def union_in_ctuple_literal():
    """
    >>> union_in_ctuple_literal()
    (1, 2.0)
    """
    cdef (Union,) a = ({"x": 1},)
    cdef (Union,) b = ({"y": 2},)
    return a[0].x, b[0].y


def union_in_ctuple_dynamic(*values):
    """
    >>> union_in_ctuple_dynamic(1, {'x': 1})
    1
    >>> union_in_ctuple_dynamic(2, {'y': 2})
    2.0
    >>> union_in_ctuple_dynamic(1, {'x': 1, 'y': 2})
    Traceback (most recent call last):
    ValueError: More than one union attribute passed: 'x' and 'y'
    """
    cdef (int, Union) a = values
    return a[1].x if a[0] == 1 else a[1].y


cdef (int, int*) cdef_ctuple_return_type(int x, int* x_ptr):
    return x, x_ptr

def call_cdef_ctuple_return_type(int x):
    """
    >>> call_cdef_ctuple_return_type(2)
    (2, 2)
    """
    cdef (int, int*) res = cdef_ctuple_return_type(x, &x)
    return res[0], res[1][0]


cpdef (int, double) cpdef_ctuple_return_type(int x, double y):
    """
    >>> cpdef_ctuple_return_type(1, 2)
    (1, 2.0)
    """
    return x, y


@cython.infer_types(True)
def test_type_inference():
    """
    >>> test_type_inference()
    """
    cdef int x = 1
    cdef double y = 2
    cdef object o = 3
    xy = (x, y)
    assert cython.typeof(xy) == "(int, double)", cython.typeof(xy)
    xo = (x, o)
    assert cython.typeof(xo) == "tuple object", cython.typeof(xo)


@cython.locals(a=(int,int), b=(cython.long,cython.float))
def test_pure_python_declaration(x, y):
    """
    >>> test_pure_python_declaration(1, 2)
    (int, int)
    (long, float)
    ((1, 2), (1, 2.0))
    >>> test_pure_python_declaration(1.0, 2.0)
    (int, int)
    (long, float)
    ((1, 2), (1, 2.0))
    >>> test_pure_python_declaration('x', 'y')
    Traceback (most recent call last):
    TypeError: an integer is required
    """
    a = (x, y)
    b = (x, y)
    print(cython.typeof(a))
    print(cython.typeof(b))
    return (a, b)


def test_equality((int, int) ab, (int, int) cd, (int, int) ef):
    """
    >>> test_equality((1, 2), (3, 4), (5, 6))
    True
    >>> test_equality((1, 2), (3, 4), (3, 4))
    True
    >>> test_equality((3, 4), (3, 4), (3, 4))
    False
    """
    return ab < cd <= ef

def test_equality_different_types((double, int) ab, (int, int) cd, (long, int) ef):
    """
    >>> test_equality((1, 2), (3, 4), (5, 6))
    True
    >>> test_equality((1, 2), (3, 4), (3, 4))
    True
    >>> test_equality((3, 4), (3, 4), (3, 4))
    False
    """
    return ab < cd <= ef

def test_binop((int, int) ab, (double, double) cd):
    """
    >>> test_binop((1, 2), (3, 4))
    (1, 2, 3.0, 4.0)
    """
    return ab + cd

def test_mul((int, int) ab, int c):
    """
    >>> test_mul((1, 2), 3)
    (1, 2, 1, 2, 1, 2)
    """
    return ab * c

def test_unop((int, int) ab):
    """
    >>> test_unop((1, 2))
    True
    """
    return not ab
