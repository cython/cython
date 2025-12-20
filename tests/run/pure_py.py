# mode: run
# cython: language_level=3

import cython
from cython import sizeof

is_compiled = cython.compiled

NULL = 5
_NULL = NULL


def test_sizeof():
    """
    >>> test_sizeof()
    True
    True
    True
    True
    True
    """
    x = cython.declare(cython.bint)
    print(cython.sizeof(x) == cython.sizeof(cython.bint))
    print(sizeof(cython.char) <= sizeof(cython.short) <= sizeof(cython.int) <= sizeof(cython.long) <= sizeof(cython.longlong))
    print(cython.sizeof(cython.uint) == cython.sizeof(cython.int))
    print(cython.sizeof(cython.p_int) == cython.sizeof(cython.p_double))
    if cython.compiled:
        print(cython.sizeof(cython.char) < cython.sizeof(cython.longlong))
    else:
        print(cython.sizeof(cython.char) == 1)


def test_declare(n):
    """
    >>> test_declare(100)
    (100, 100, 100)
    >>> test_declare(100.5)
    (100, 100, 100)
    """
    x = cython.declare(cython.int)
    y = cython.declare(cython.int, n)
    z = cython.declare(int, n)  # C int
    if cython.compiled:
        cython.declare(xx=cython.int, yy=cython.long)
        i = cython.sizeof(xx)
    ptr = cython.declare(cython.p_int, cython.address(y))
    return y, z, ptr[0]


@cython.locals(x=cython.double, n=cython.int)
def test_cast(x):
    """
    >>> test_cast(1.5)
    1
    """
    n = cython.cast(cython.int, x)
    return n


@cython.locals(x=cython.int, y=cython.p_int)
def test_address(x):
    """
    >>> test_address(39)
    39
    """
    y = cython.address(x)
    return y[0]


@cython.wraparound(False)
def test_wraparound(x):
    """
    >>> test_wraparound([1, 2, 3])
    [1, 2, 1]
    """
    with cython.wraparound(True):
        x[-1] = x[0]
    return x


@cython.boundscheck(False)
def test_boundscheck(x):
    """
    >>> test_boundscheck([1, 2, 3])
    3
    >>> try: test_boundscheck([1, 2])
    ... except IndexError: pass
    """
    with cython.boundscheck(True):
        return x[2]


## CURRENTLY BROKEN - FIXME!!
## Is this test make sense? Implicit conversion in pure Python??

## @cython.locals(x=cython.int)
## @cython.locals(y=cython.bint)
## def test_locals(x):
##     """
##     >>> test_locals(5)
##     True
##     """
##     y = x
##     return y


def test_with_nogil(nogil, should_raise=False):
    """
    >>> raised = []
    >>> class nogil(object):
    ...     def __enter__(self):
    ...         pass
    ...     def __exit__(self, exc_class, exc, tb):
    ...         raised.append(exc)
    ...         return exc_class is None

    >>> test_with_nogil(nogil())
    WORKS
    True
    >>> raised
    [None]

    >>> test_with_nogil(nogil(), should_raise=True)
    Traceback (most recent call last):
    ValueError: RAISED!

    >>> raised[1] is None
    False
    """
    result = False
    should_raise_bool = True if should_raise else False  # help the type inference ...
    with nogil:
        print("WORKS")
        with cython.nogil:
            result = True
            if should_raise_bool:
                raise ValueError("RAISED!")
    return result


MyUnion = cython.union(n=cython.int, x=cython.double)
MyStruct = cython.struct(is_integral=cython.bint, data=MyUnion)
MyStruct2 = cython.typedef(MyStruct[2])
MyStruct3 = cython.typedef(MyStruct[3])

def test_struct(n, x):
    """
    >>> test_struct(389, 1.64493)
    (389, 1.64493, False)
    """
    a = cython.declare(MyStruct3)
    a[0] = MyStruct(is_integral=True, data=MyUnion(n=n))
    a[1] = MyStruct(is_integral=False, data={'x': x})
    # dict is ordered => struct creation via keyword arguments above was deterministic!
    a[2] = MyStruct(False, MyUnion(x=x))
    return a[0].data.n, a[1].data.x, a[2].is_integral

import cython as cy
from cython import declare, cast, locals, address, typedef, p_void, compiled
from cython import declare as my_declare, locals as my_locals, p_void as my_void_star, typedef as my_typedef, compiled as my_compiled

@my_locals(a=cython.p_void)
def test_imports():
    """
    >>> test_imports()
    (True, True)
    """
    a = cython.NULL
    b = declare(p_void, cython.NULL)
    c = my_declare(my_void_star, cython.NULL)
    d = cy.declare(cy.p_void, cython.NULL)

    return a == d, compiled == my_compiled

## CURRENTLY BROKEN - FIXME!!

# MyStruct3 = typedef(MyStruct[3])
# MyStruct4 = my_typedef(MyStruct[4])
# MyStruct5 = cy.typedef(MyStruct[5])

def test_declare_c_types(n):
    """
    >>> test_declare_c_types(0)
    >>> test_declare_c_types(1)
    >>> test_declare_c_types(2)
    """
    #
    b00 = cython.declare(cython.bint, 0)
    b01 = cython.declare(cython.bint, 1)
    b02 = cython.declare(cython.bint, 2)
    #
    i00 = cython.declare(cython.uchar, n)
    i01 = cython.declare(cython.char, n)
    i02 = cython.declare(cython.schar, n)
    i03 = cython.declare(cython.ushort, n)
    i04 = cython.declare(cython.short, n)
    i05 = cython.declare(cython.sshort, n)
    i06 = cython.declare(cython.uint, n)
    i07 = cython.declare(cython.int, n)
    i08 = cython.declare(cython.sint, n)
    i09 = cython.declare(cython.slong, n)
    i10 = cython.declare(cython.long, n)
    i11 = cython.declare(cython.ulong, n)
    i12 = cython.declare(cython.slonglong, n)
    i13 = cython.declare(cython.longlong, n)
    i14 = cython.declare(cython.ulonglong, n)

    i20 = cython.declare(cython.Py_ssize_t, n)
    i21 = cython.declare(cython.size_t, n)
    #
    f00 = cython.declare(cython.float, n)
    f01 = cython.declare(cython.double, n)
    f02 = cython.declare(cython.longdouble, n)
    #
    #z00 = cython.declare(cython.complex, n+1j)
    #z01 = cython.declare(cython.floatcomplex, n+1j)
    #z02 = cython.declare(cython.doublecomplex, n+1j)
    #z03 = cython.declare(cython.longdoublecomplex, n+1j)


@cython.ccall
@cython.returns(cython.double)
def c_call(x):
    if x == -2.0:
        raise RuntimeError("huhu!")
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

    >>> call_ccall(-2)
    Traceback (most recent call last):
    RuntimeError: huhu!
    """
    ret = c_call(x)
    return ret, cython.typeof(ret)


@cython.cfunc
@cython.inline
@cython.returns(cython.double)
def cdef_inline(x):
    if x == -2.0:
        raise RuntimeError("huhu!")
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

    >>> call_cdef_inline(-2)
    Traceback (most recent call last):
    RuntimeError: huhu!
    """
    ret = cdef_inline(x)
    return ret, cython.typeof(ret)


@cython.cfunc
@cython.nogil
@cython.locals(x=cython.int)
@cython.returns(cython.int)
def cdef_nogil(x):
    return x + 1


@cython.cfunc
@cython.nogil(True)
@cython.locals(x=cython.int)
@cython.returns(cython.int)
def cdef_nogil_true(x):
    return x + 1


@cython.cfunc
@cython.nogil(False)
@cython.locals(x=cython.int)
@cython.returns(cython.int)
def cdef_nogil_false(x):
    return x + 1


@cython.locals(x=cython.int, result=cython.int)
def test_cdef_nogil(x):
    """
    >>> test_cdef_nogil(5)
    24
    """
    with cython.nogil:
        result = cdef_nogil(x)
    with cython.nogil(True):
        result += cdef_nogil_true(x)
    with cython.nogil(False), cython.nogil(True), cython.gil(False):
        result += cdef_nogil(x)
    result += cdef_nogil_false(x)
    return result


@cython.cfunc
@cython.inline
def has_inner_func(x):
    # the inner function must remain a Python function
    # (and inline must not be applied to it)
    @cython.test_fail_if_path_exists("//CFuncDefNode")
    def inner():
        return x
    return inner


def test_has_inner_func():
    """
    >>> test_has_inner_func()
    1
    """
    return has_inner_func(1)()


@cython.locals(counts=cython.int[10], digit=cython.int)
def count_digits_in_carray(digits):
    """
    >>> digits = '37692837651902834128342341'
    >>> ''.join(sorted(digits))
    '01112222333334445667788899'
    >>> count_digits_in_carray(map(int, digits))
    [1, 3, 4, 5, 3, 1, 2, 2, 3, 2]
    """
    counts = [0] * 10
    for digit in digits:
        assert 0 <= digit <= 9
        counts[digit] += 1
    return counts


@cython.test_assert_path_exists("//CFuncDeclaratorNode//IntNode[@base_10_value = '-1']")
@cython.ccall
@cython.returns(cython.long)
@cython.exceptval(-1)
def ccall_except(x):
    """
    >>> ccall_except(41)
    42
    >>> ccall_except(0)
    Traceback (most recent call last):
    ValueError
    """
    if x == 0:
        raise ValueError
    return x+1


@cython.test_assert_path_exists("//CFuncDeclaratorNode//IntNode[@base_10_value = '-1']")
@cython.cfunc
@cython.returns(cython.long)
@cython.exceptval(-1)
def cdef_except(x):
    if x == 0:
        raise ValueError
    return x+1


def call_cdef_except(x):
    """
    >>> call_cdef_except(41)
    42
    >>> call_cdef_except(0)
    Traceback (most recent call last):
    ValueError
    """
    return cdef_except(x)


@cython.test_assert_path_exists("//CFuncDeclaratorNode//IntNode[@base_10_value = '-1']")
@cython.ccall
@cython.returns(cython.long)
@cython.exceptval(-1, check=True)
def ccall_except_check(x):
    """
    >>> ccall_except_check(41)
    42
    >>> ccall_except_check(-2)
    -1
    >>> ccall_except_check(0)
    Traceback (most recent call last):
    ValueError
    """
    if x == 0:
        raise ValueError
    return x+1


@cython.test_assert_path_exists("//CFuncDeclaratorNode")
@cython.ccall
@cython.returns(cython.long)
@cython.exceptval(check=True)
def ccall_except_check_always(x):
    """
    Note that this actually takes the same shortcut as for a Cython-syntax cdef function
    and does except ?-1

    >>> ccall_except_check_always(41)
    42
    >>> ccall_except_check_always(0)
    Traceback (most recent call last):
    ValueError
    """
    if x == 0:
        raise ValueError
    return x+1


@cython.test_fail_if_path_exists("//CFuncDeclaratorNode//IntNode[@base_10_value = '-1']")
@cython.test_assert_path_exists("//CFuncDeclaratorNode")
@cython.ccall
@cython.returns(cython.long)
@cython.exceptval(check=False)
def ccall_except_no_check(x):
    """
    >>> ccall_except_no_check(41)
    42
    >>> try: _ = ccall_except_no_check(0)  # no exception propagated!
    ... except ValueError: assert not is_compiled
    """
    if x == 0:
        raise ValueError
    return x+1


@cython.final
@cython.cclass
class CClass(object):
    """
    >>> c = CClass(2)
    >>> c.get_attr()
    int
    2
    """
    cython.declare(attr=cython.int)

    def __init__(self, attr):
        self.attr = attr

    def get_attr(self):
        print(cython.typeof(self.attr))
        return self.attr


class TestUnboundMethod:
    """
    >>> C = TestUnboundMethod
    >>> C.meth is C.__dict__["meth"]
    True
    """
    def meth(self): pass

@cython.cclass
class Foo:
    a = cython.declare(cython.double)
    b = cython.declare(cython.double)
    c = cython.declare(cython.double)

    @cython.locals(a=cython.double, b=cython.double, c=cython.double)
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

@cython.cclass
class EmptyClass(object):
    def __init__(self, *args):
        pass

def same_type_cast():
    """
    >>> same_type_cast()
    True
    """

    f = EmptyClass()
    return f is cython.cast(EmptyClass, f)

def multi_args_init_cast():
    """
    >>> multi_args_init_cast()
    True
    """
    f = Foo(10, 20, 30)
    return cython.cast(Foo, f) is f

def multi_args_init_declare():
    """
    >>> multi_args_init_declare() is None
    True
    """
    f = cython.declare(Foo)

    if cython.compiled:
        f = None

    return f

EmptyClassSyn = cython.typedef(EmptyClass)

def empty_declare():
    """
    >>> empty_declare()
    []
    """

    r0 = cython.declare(EmptyClass)
    r1 = cython.declare(EmptyClassSyn)
    r2 = cython.declare(MyStruct)
    r3 = cython.declare(MyUnion)
    r4 = cython.declare(MyStruct2)
    r5 = cython.declare(cython.int[2])

    if cython.compiled:
        r0 = None
        r1 = None

    res = [
        r0 is None,
        r1 is None,
        r2 is not None,
        r3 is not None,
        r4 is not None,
        r5 is not None
    ]

    r2.is_integral = True
    assert r2.is_integral == True

    r3.x = 12.3
    assert r3.x == 12.3

    #It generates a correct C code, but raises an exception when interpreted
    if cython.compiled:
        r4[0].is_integral = True
        assert r4[0].is_integral == True

    r5[0] = 42
    assert r5[0] == 42

    return [i for i, x in enumerate(res) if not x]

def same_declare():
    """
    >>> same_declare()
    True
    """

    f = EmptyClass()
    f2 = cython.declare(EmptyClass, f)
    return f2 is f

def none_cast():
    """
    >>> none_cast() is None
    True
    """

    f = None
    return cython.cast(EmptyClass, f)

def none_declare():
    """
    >>> none_declare() is None
    True
    """

    f = None
    f2 = cython.declare(Foo, f)
    return f2

def array_init_with_list():
    """
    >>> array_init_with_list()
    [10, 42]
    """
    x = cython.declare(cython.int[20], list(range(20)))
    x[12] = 42

    return [x[10], x[12]]
