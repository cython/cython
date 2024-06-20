# mode: run
# tag: warnings

import cython

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
    print sizeof(x) == sizeof(cython.bint)
    print sizeof(cython.char) <= sizeof(cython.short) <= sizeof(cython.int) <= sizeof(cython.long) <= sizeof(cython.longlong)
    print sizeof(cython.uint) == sizeof(cython.int)
    print sizeof(cython.p_int) == sizeof(cython.p_double)
    if cython.compiled:
        print sizeof(cython.char) < sizeof(cython.longlong)
    else:
        print sizeof(cython.char) == 1

def test_declare(n):
    """
    >>> test_declare(100)
    (100, 100)
    >>> test_declare(100.5)
    (100, 100)

    # CPython: "TypeError: an integer is required"
    >>> test_declare(None) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: ...int...
    """
    x = cython.declare(cython.int)
    y = cython.declare(cython.int, n)
    if cython.compiled:
        cython.declare(xx=cython.int, yy=cython.long)
        i = sizeof(xx)
    ptr = cython.declare(cython.p_int, cython.address(y))
    return y, ptr[0]

@cython.locals(x=cython.double, n=cython.int)
def test_cast(x):
    """
    >>> test_cast(1.5)
    1
    >>> try: test_cast(None)
    ... except TypeError: pass
    """
    n = cython.cast(cython.int, x)
    return n

@cython.locals(as_list=list)
def test_cast_object(x, typecheck):
    """
    >>> test_cast_object([1, 2, 3], True)
    [1, 2, 3]
    >>> test_cast_object([1, 2, 3], False)
    [1, 2, 3]
    >>> test_cast_object((1, 2, 3), True)
    Traceback (most recent call last):
    ...
    TypeError: Expected list, got tuple
    >>> test_cast_object((1, 2, 3), False)
    (1, 2, 3)
    """
    if typecheck:
        as_list = cython.cast(list, x, typecheck=True)
    else:
        as_list = cython.cast(list, x, typecheck=False)
    return as_list

@cython.locals(x=cython.int, y=cython.p_int)
def test_address(x):
    """
    >>> test_address(39)
    39
    """
    y = cython.address(x)
    return y[0]

@cython.locals(x=cython.int)
@cython.locals(y=cython.bint)
def test_locals(x):
    """
    >>> test_locals(5)
    True
    """
    y = x
    return y

MyUnion = cython.union(n=cython.int, x=cython.double)
MyStruct = cython.struct(is_integral=cython.bint, data=MyUnion)
MyStruct2 = cython.typedef(MyStruct[2])

def test_struct(n, x):
    """
    >>> test_struct(389, 1.64493)
    (389, 1.64493)
    """
    a = cython.declare(MyStruct2)
    a[0] = MyStruct(True, data=MyUnion(n=n))
    a[1] = MyStruct(is_integral=False, data={'x': x})
    return a[0].data.n, a[1].data.x

import cython as cy
from cython import declare, cast, locals, address, typedef, p_void, compiled
from cython import declare as my_declare, locals as my_locals, p_void as my_void_star, typedef as my_typedef, compiled as my_compiled

@my_locals(a=cython.p_void)
def test_imports():
    """
    >>> test_imports()
    True
    """
    a = cython.NULL
    b = declare(p_void, cython.NULL)
    c = my_declare(my_void_star, cython.NULL)
    d = cy.declare(cy.p_void, cython.NULL)
    return a == d and compiled and my_compiled

MyStruct3 = typedef(MyStruct[3])
MyStruct4 = my_typedef(MyStruct[4])
MyStruct5 = cy.typedef(MyStruct[5])

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


cdef class ExtType:
    """
    >>> x = ExtType()
    >>> x.forward_ref(x)
    'ExtType'
    """
    @cython.locals(x="ExtType")
    def forward_ref(self, x):
        return cython.typeof(x)


def ext_type_string_ref(x: "ExtType"):
    """
    >>> x = ExtType()
    >>> ext_type_string_ref(x)
    'ExtType'
    """
    return cython.typeof(x)


with cython.cdivision(True):

    @cython.cdivision(False)
    @cython.cdivision(True)
    def test_override_reset(x: cython.int):
        """
        >>> test_override_reset(-3)  # @cdivision(False)
        -2
        """
        return x / 2

    @cython.cdivision(True)
    @cython.cdivision(False)
    def test_override_set(x: cython.int):
        """
        >>> test_override_set(-5)  # @cdivision(True)
        -1
        """
        return x / 3

    @cython.cdivision(True)
    @cython.cdivision(False)
    @cython.cdivision(True)
    @cython.cdivision(False)
    @cython.cdivision(False)
    @cython.cdivision(False)
    @cython.cdivision(True)
    @cython.cdivision(False)
    @cython.cdivision(True)
    @cython.cdivision(True)
    @cython.cdivision(True)
    @cython.cdivision(False)
    def test_override_set_repeated(x: cython.int):
        """
        >>> test_override_set_repeated(-5)  # @cdivision(True)
        -1
        """
        return x / 3


_WARNINGS = """
181:27: Strings should no longer be used for type declarations. Use 'cython.int' etc. directly.
193:4: Directive does not change previous value (cdivision=True)
213:4: Directive does not change previous value (cdivision=False)
214:4: Directive does not change previous value (cdivision=False)
218:4: Directive does not change previous value (cdivision=True)
219:4: Directive does not change previous value (cdivision=True)
"""
