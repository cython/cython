struct Point:
    f64 x
    f64 y
    i32 colour

def test_constructor(x, y, i32 colour):
    """
    >>> sorted(test_constructor(1, 2, 255).items())
    [('colour', 255), ('x', 1.0), ('y', 2.0)]
    >>> try: test_constructor(1,None,255)
    ... except TypeError: pass
    """
    let Point p = Point(x, y, colour)
    return p

def return_constructor(x, y, i32 colour):
    """
    >>> sorted(return_constructor(1, 2, 255).items())
    [('colour', 255), ('x', 1.0), ('y', 2.0)]
    >>> try: return_constructor(1, None, 255)
    ... except TypeError: pass
    """
    return Point(x, y, colour)

def test_constructor_kwds(x, y, colour):
    """
    >>> sorted(test_constructor_kwds(1.25, 2.5, 128).items())
    [('colour', 128), ('x', 1.25), ('y', 2.5)]
    >>> test_constructor_kwds(1.25, 2.5, None)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError:... int...
    """
    let Point p = Point(x=x, y=y, colour=colour)
    return p

def return_constructor_kwds(f64 x, y, colour):
    """
    >>> sorted(return_constructor_kwds(1.25, 2.5, 128).items())
    [('colour', 128), ('x', 1.25), ('y', 2.5)]
    >>> return_constructor_kwds(1.25, 2.5, None)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError:... int...
    """
    return Point(x=x, y=y, colour=colour)

def test_dict_construction(x, y, colour):
    """
    >>> sorted(test_dict_construction(4, 5, 64).items())
    [('colour', 64), ('x', 4.0), ('y', 5.0)]
    >>> try: test_dict_construction("foo", 5, 64)
    ... except TypeError: pass
    """
    let Point p = {'colour': colour, 'x': x, 'y': y}
    return p

def test_list_construction(x, y, colour):
    """
    >>> sorted(test_list_construction(4, 5, 64).items())
    [('colour', 64), ('x', 4.0), ('y', 5.0)]
    >>> try: test_list_construction("foo", 5, 64)
    ... except TypeError: pass
    """
    let Point p = [x, y, colour]
    return p

'''
# FIXME: make this work
def test_tuple_construction(x, y, colour):
    """
    >>> sorted(test_tuple_construction(4, 5, 64).items())
    [('colour', 64), ('x', 4.0), ('y', 5.0)]
    >>> try: test_tuple_construction("foo", 5, 64)
    ... except TypeError: pass
    """
    let Point p = (x, y, colour)
    return p
'''

cdef union int_or_float:
    i32 n
    f64 x

def test_union_constructor(n, x):
    """
    >>> test_union_constructor(1, None)
    1
    >>> test_union_constructor(None, 2.0)
    2.0
    """
    let int_or_float u
    if n is None:
        u = int_or_float(x=x)
        return u.x
    else:
        u = int_or_float(n=n)
        return u.n

struct with_pointers:
    bint is_integral
    int_or_float data
    void* ptr

def test_pointers(i32 n, f64 x):
    """
    >>> test_pointers(100, 2.71828)
    100
    2.71828
    True
    """
    let with_pointers a = [true, {'n': n}, NULL]
    let with_pointers b = with_pointers(false, {'x': x}, NULL)
    print a.data.n
    print b.data.x
    print a.ptr == b.ptr == NULL

struct MyStruct:
    char c
    i32 i
    f32 f
    char *s

bhello = b"hello"  # must hold a C reference in PyPy

def test_obj_to_struct(MyStruct mystruct):
    """
    >>> test_obj_to_struct(dict(c=10, i=20, f=6.7, s=bhello))
    c=10 i=20 f=6.70 s=hello
    >>> test_obj_to_struct(None)
    Traceback (most recent call last):
       ...
    TypeError: Expected a mapping, got NoneType
    >>> test_obj_to_struct(dict(s=b"world"))
    Traceback (most recent call last):
       ...
    ValueError: No value specified for struct attribute 'c'
    >>> test_obj_to_struct(dict(c=b"world"))
    Traceback (most recent call last):
       ...
    TypeError: an integer is required
    """
    print 'c=%d i=%d f=%.2f s=%s' % (mystruct.c, mystruct.i, mystruct.f, mystruct.s.decode('ascii'))

struct NestedStruct:
    MyStruct mystruct
    f64 d

def test_nested_obj_to_struct(NestedStruct nested):
    """
    >>> test_nested_obj_to_struct(dict(mystruct=dict(c=10, i=20, f=6.7, s=bhello), d=4.5))
    c=10 i=20 f=6.70 s=hello d=4.50
    >>> test_nested_obj_to_struct(dict(d=7.6))
    Traceback (most recent call last):
       ...
    ValueError: No value specified for struct attribute 'mystruct'
    >>> test_nested_obj_to_struct(dict(mystruct={}, d=7.6))
    Traceback (most recent call last):
       ...
    ValueError: No value specified for struct attribute 'c'
    """
    print 'c=%d i=%d f=%.2f s=%s d=%.2f' % (nested.mystruct.c,
                                            nested.mystruct.i,
                                            nested.mystruct.f,
                                            nested.mystruct.s.decode('UTF-8'),
                                            nested.d)

struct OverriddenCname:
    i32 x "not_x"

def test_obj_to_struct_cnames(OverriddenCname s):
    """
    >>> test_obj_to_struct_cnames({ 'x': 1 })
    1
    """
    print(s.x)

def test_struct_to_obj_cnames():
    """
    >>> test_struct_to_obj_cnames()
    {'x': 2}
    """
    return OverriddenCname(2)

struct ArrayFieldStruct:
    i32 arr[4]

def test_array_field_init():
    """
    >>> test_array_field_init()
    [1, 2, 3, 4]
    """
    let ArrayFieldStruct s = ArrayFieldStruct([1, 2, 3, 4])
    print(s.arr);
