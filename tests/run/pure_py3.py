# mode: run
# tag: annotation_typing, pure3.0, mypy

import cython

is_compiled = cython.compiled

MyUnion = cython.union(n=cython.int, x=cython.double)
MyStruct = cython.struct(is_integral=cython.bint, data=MyUnion)
MyStruct2 = cython.typedef(MyStruct[2])


@cython.annotation_typing(False)
def test_annotation_typing(x: cython.int) -> cython.int:
    """
    >>> test_annotation_typing("Petits pains")
    'Petits pains'
    """
    return x


@cython.ccall  # cpdef => C return type
def test_return_type(n: cython.int) -> cython.double:
    """
    >>> test_return_type(389)
    389.0
    """
    assert cython.typeof(n) == 'int', cython.typeof(n)
    return n if is_compiled else float(n)


# Using a variable (which MyStruct2 = cython.typedef(MyStruct[2]) becomes) as an annotation
# is invalid but there is no other way of defining type definitions to Cython right now.
def test_struct(n: cython.int, x: cython.double) -> MyStruct2:  # type: ignore
    """
    >>> test_struct(389, 1.64493)
    (389, 1.64493)
    >>> d = test_struct.__annotations__
    >>> sorted(d)
    ['n', 'return', 'x']
    """
    assert cython.typeof(n) == 'int', cython.typeof(n)
    if is_compiled:
        assert cython.typeof(x) == 'double', cython.typeof(x)  # C double
    else:
        assert cython.typeof(x) == 'float', cython.typeof(x)   # Python float

    a = cython.declare(MyStruct2)
    a[0] = MyStruct(is_integral=True, data=MyUnion(n=n))
    a[1] = MyStruct(is_integral=False, data={'x': x})
    return a[0].data.n, a[1].data.x


@cython.ccall
def c_call(x) -> cython.double:
    return x


def call_ccall(x):
    """
    Test that a declared return type is honoured when compiled.

    >>> result, return_type = call_ccall(1)

    >>> (not is_compiled and 'double') or return_type
    'double'
    >>> (is_compiled and 'int') or return_type
    'int'

    >>> (not is_compiled and 1.0) or result
    1.0
    >>> (is_compiled and 1) or result
    1
    """
    ret = c_call(x)
    return ret, cython.typeof(ret)


@cython.cfunc
@cython.inline
def cdef_inline(x) -> cython.double:
    return x + 1


def call_cdef_inline(x):
    """
    >>> result, return_type = call_cdef_inline(1)
    >>> (not is_compiled and 'float') or type(result).__name__
    'float'
    >>> (not is_compiled and 'double') or return_type
    'double'
    >>> (is_compiled and 'int') or return_type
    'int'
    >>> result == 2.0  or  result
    True
    """
    ret = cdef_inline(x)
    return ret, cython.typeof(ret)

@cython.cfunc
def test_cdef_return_object(x: object) -> object:
    """
    Test support of python object in annotations
    >>> test_cdef_return_object(3)
    3
    >>> test_cdef_return_object(None)
    Traceback (most recent call last):
        ...
    RuntimeError
    """
    if x:
        return x
    else:
        raise RuntimeError()


def test_pointer_const_volatile(c_string: cython.p_const_char):
    """
    >>> test_pointer_const_volatile(b'xyz')
    const char *
    int
    volatile int
    int *
    const int *
    b'xyz'
    """
    # Using 'int' since that looks the same in Python and Cython.
    a: cython.int = 5
    a_v: cython.volatile[cython.int] = 7
    p: cython.pointer[cython.int] = cython.NULL
    p_c: cython.pointer[cython.const[cython.int]] = cython.NULL

    # additional compile test (cannot assign initial value):
    a_c: cython.const[cython.pointer[cython.const[cython.int]]]

    print(cython.typeof(c_string) if cython.compiled else "const char *")
    print(cython.typeof(a))
    print(cython.typeof(a_v) if cython.compiled else f"volatile {cython.typeof(a_v)}")

    print(cython.typeof(p) if cython.compiled else "int *")
    print(cython.typeof(p_c) if cython.compiled else "const int *")
    return c_string
