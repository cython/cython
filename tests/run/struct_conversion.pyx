cdef struct Point:
    double x
    double y
    int color

def test_constructor(x, y, color):
    """
    >>> test_constructor(1,2,255)
    {'y': 2.0, 'x': 1.0, 'color': 255}
    >>> test_constructor(1,None,255)
    Traceback (most recent call last):
    ...
    TypeError: a float is required
    """
    cdef Point p = Point(x, y, color)
    return p

def test_constructor_kwds(x, y, color):
    """
    >>> test_constructor_kwds(1.25, 2.5, 128)
    {'y': 2.5, 'x': 1.25, 'color': 128}
    >>> test_constructor_kwds(1.25, 2.5, None)
    Traceback (most recent call last):
    ...
    TypeError: an integer is required
    """
    cdef Point p = Point(x=x, y=y, color=color)
    return p

def test_dict_construction(x, y, color):
    """
    >>> test_dict_construction(4, 5, 64)
    {'y': 5.0, 'x': 4.0, 'color': 64}
    >>> test_dict_construction("foo", 5, 64)
    Traceback (most recent call last):
    ...
    TypeError: a float is required
    """
    cdef Point p = {'color': color, 'x': x, 'y': y}
    return p

cdef union int_or_float:
    int n
    double x

cdef struct with_pointers:
    bint is_integral
    int_or_float data
    void* ptr

def test_pointers(int n, double x):
    """
    >>> test_pointers(100, 2.71828)
    100
    2.71828
    True
    """
    cdef with_pointers a = [True, {'n': n}, NULL]
    cdef with_pointers b = with_pointers(False, {'x': x}, NULL)
    print a.data.n
    print b.data.x
    print a.ptr == b.ptr == NULL
