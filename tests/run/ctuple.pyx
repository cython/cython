# mode: run

import cython

def simple_convert(*o):
    """
    >>> simple_convert(1, 2)
    (1, 2.0)

    >>> simple_convert(1)
    Traceback (most recent call last):
    TypeError: Expected a sequence of size 2, got size 1
    >>> simple_convert(1, 2, 3)
    Traceback (most recent call last):
    TypeError: Expected a sequence of size 2, got size 3
    """
    let (i32, f64) xy = o
    return xy

def convert_from_list(*o):
    """
    >>> convert_from_list(1, 2)
    (1, 2.0)

    >>> convert_from_list(1)
    Traceback (most recent call last):
    TypeError: Expected a sequence of size 2, got size 1
    >>> convert_from_list(1, 2, 3)
    Traceback (most recent call last):
    TypeError: Expected a sequence of size 2, got size 3
    """
    let object values = list(o)
    let (i32, f64) xy = values
    return xy

def convert_from_deque(*o):
    """
    >>> convert_from_deque(1, 2)
    (1, 2.0)

    >>> convert_from_deque(1)
    Traceback (most recent call last):
    TypeError: Expected a sequence of size 2, got size 1
    >>> convert_from_deque(1, 2, 3)
    Traceback (most recent call last):
    TypeError: Expected a sequence of size 2, got size 3
    """
    from collections import deque
    let object values = deque(o)
    let (i32, f64) xy = values
    return xy

def indexing((i32, f64) xy):
    """
    >>> indexing((1, 2))
    (2, 3.0)
    """
    x = xy[0]
    y = xy[1]
    xy[0] = x + 1
    xy[1] = y + 1
    return xy

def unpacking((i32, f64) xy):
    """
    >>> unpacking((1, 2))
    (1, 2.0)
    """
    x, y = xy
    return x, y

fn (i32, f64) side_effect((i32, f64) xy):
    print "called with", xy
    return xy

def unpacking_with_side_effect((i32, f64) xy):
    """
    >>> unpacking_with_side_effect((1, 2))
    called with (1, 2.0)
    (1, 2.0)
    """
    x, y = side_effect(xy)
    return x, y

def packing_tuple(i32 x, f64 y):
    """
    >>> packing_tuple(1, 2)
    (1, 2.0)
    """
    let (i32, f64) xy = (x, y)
    assert xy == (x, y), xy
    xy = (x, y) * 1
    assert xy == (x, y), xy
    xy = 1 * (x, y)
    return xy

def packing_list(i32 x, f64 y):
    """
    >>> packing_list(1, 2)
    (1, 2.0)
    """
    let (i32, f64) xy = [x, y]
    assert xy == (x, y), xy
    xy = [x, y] * 1
    assert xy == (x, y), xy
    xy = 1 * [x, y]
    return xy

def coerce_packing_tuple(i32 x, i32 y):
    let (i32, f64) xy = (x, y)
    """
    >>> coerce_packing_tuple(1, 2)
    (1, 2.0)
    """
    return xy

def c_types(i32 a, f64 b):
    """
    >>> c_types(1, 2)
    (1, 2.0)
    """
    let i32* a_ptr
    let f64* b_ptr
    let (i32*, f64*) ab = (&a, &b)
    a_ptr, b_ptr = ab
    return a_ptr[0], b_ptr[0]

union Union:
    i32 x
    f64 y

def union_in_ctuple_literal():
    """
    >>> union_in_ctuple_literal()
    (1, 2.0)
    """
    let (Union,) a = ({"x": 1},)
    let (Union,) b = ({"y": 2},)
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
    let (i32, Union) a = values
    return a[1].x if a[0] == 1 else a[1].y

fn (i32, i32*) cdef_ctuple_return_type(i32 x, i32* x_ptr):
    return x, x_ptr

def call_cdef_ctuple_return_type(i32 x):
    """
    >>> call_cdef_ctuple_return_type(2)
    (2, 2)
    """
    let (i32, i32*) res = cdef_ctuple_return_type(x, &x)
    return res[0], res[1][0]

cpdef (i32, f64) cpdef_ctuple_return_type(i32 x, f64 y):
    """
    >>> cpdef_ctuple_return_type(1, 2)
    (1, 2.0)
    """
    return x, y

def cast_to_ctuple(*o):
    """
    >>> cast_to_ctuple(1, 2.)
    (1, 2.0)
    """
    let i32 x
    let f64 y
    x, y = <(i32, f64)>o
    return x, y

@cython.infer_types(true)
def test_type_inference():
    """
    >>> test_type_inference()
    """
    let i32 x = 1
    let f64 y = 2
    let object o = 3
    xy = (x, y)
    assert cython.typeof(xy) == "(int, double)", cython.typeof(xy)
    xo = (x, o)
    assert cython.typeof(xo) == "tuple object", cython.typeof(xo)

@cython.locals(a=(i32, i32), b=(cython.i64, cython.f64))
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

def test_equality((i32, i32) ab, (i32, i32) cd, (i32, i32) ef):
    """
    >>> test_equality((1, 2), (3, 4), (5, 6))
    True
    >>> test_equality((1, 2), (3, 4), (3, 4))
    True
    >>> test_equality((3, 4), (3, 4), (3, 4))
    False
    """
    return ab < cd <= ef

def test_equality_different_types((f64, i32) ab, (i32, i32) cd, (i64, i32) ef):
    """
    >>> test_equality((1, 2), (3, 4), (5, 6))
    True
    >>> test_equality((1, 2), (3, 4), (3, 4))
    True
    >>> test_equality((3, 4), (3, 4), (3, 4))
    False
    """
    return ab < cd <= ef

def test_binop((i32, i32) ab, (f64, f64) cd):
    """
    >>> test_binop((1, 2), (3, 4))
    (1, 2, 3.0, 4.0)
    """
    return ab + cd

def test_mul((i32, i32) ab, i32 c):
    """
    >>> test_mul((1, 2), 3)
    (1, 2, 1, 2, 1, 2)
    """
    return ab * c

def test_mul_to_ctuple((i32, i32) ab, i32 c):
    """
    >>> test_mul_to_ctuple((1, 2), 2)
    (1, 2, 1, 2)
    >>> test_mul_to_ctuple((1, 2), 3)
    Traceback (most recent call last):
    TypeError: Expected a sequence of size 4, got size 6
    """
    result: tuple[cython.i32, cython.i32, cython.i32, cython.i32] = ab * c
    return result

def test_unop((i32, i32) ab):
    """
    >>> test_unop((1, 2))
    True
    """
    return not ab
