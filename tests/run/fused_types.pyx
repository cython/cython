# mode: run
# ticket: 1772
# cython: language_level=3str

cimport cython
from cython.view cimport array

from cython cimport integral
from cpython cimport Py_INCREF

from Cython import Shadow as pure_cython
ctypedef char * string_t

# floating = cython.fused_type(float, double) floating
# integral = cython.fused_type(int, long) integral
ctypedef cython.floating floating
fused_type1 = cython.fused_type(int, long, float, double, string_t)
fused_type2 = cython.fused_type(string_t)
ctypedef fused_type1 *composed_t
other_t = cython.fused_type(int, double)
ctypedef double *p_double
ctypedef int *p_int
fused_type3 = cython.fused_type(int, double)
fused_composite = cython.fused_type(fused_type2, fused_type3)
just_float = cython.fused_type(float)

ctypedef int inttypedef
ctypedef double doubletypedef
fused_with_typedef = cython.fused_type(inttypedef, doubletypedef)

ctypedef float const_inttypedef  # misleading name
fused_misleading_name = cython.fused_type(const_inttypedef, char)


def test_pure():
    """
    >>> test_pure()
    10
    """
    mytype = pure_cython.typedef(pure_cython.fused_type(int, complex))
    print(mytype(10))


cdef cdef_func_with_fused_args(fused_type1 x, fused_type1 y, fused_type2 z):
    if fused_type1 is string_t:
        print(x.decode('ascii'), y.decode('ascii'), z.decode('ascii'))
    else:
        print(x, y, z.decode('ascii'))

    return x + y

def test_cdef_func_with_fused_args():
    """
    >>> test_cdef_func_with_fused_args()
    spam ham eggs
    spamham
    10 20 butter
    30
    4.2 8.6 bunny
    12.8
    """
    print(cdef_func_with_fused_args(b'spam', b'ham', b'eggs').decode('ascii'))
    print(cdef_func_with_fused_args(10, 20, b'butter'))
    print(cdef_func_with_fused_args(4.2, 8.6, b'bunny'))

cdef fused_type1 fused_with_pointer(fused_type1 *array):
    for i in range(5):
        if fused_type1 is string_t:
            print(array[i].decode('ascii'))
        else:
            print(array[i])

    obj = array[0] + array[1] + array[2] + array[3] + array[4]
    # if cython.typeof(fused_type1) is string_t:
    Py_INCREF(obj)
    return obj

def test_fused_with_pointer():
    """
    >>> test_fused_with_pointer()
    0
    1
    2
    3
    4
    10
    <BLANKLINE>
    0
    1
    2
    3
    4
    10
    <BLANKLINE>
    0.0
    1.0
    2.0
    3.0
    4.0
    10.0
    <BLANKLINE>
    humpty
    dumpty
    fall
    splatch
    breakfast
    humptydumptyfallsplatchbreakfast
    """
    cdef int[5] int_array
    cdef long[5] long_array
    cdef float[5] float_array
    cdef string_t[5] string_array

    cdef char *s

    strings = [b"humpty", b"dumpty", b"fall", b"splatch", b"breakfast"]

    for i in range(5):
        int_array[i] = i
        long_array[i] = i
        float_array[i] = i
        s = strings[i]
        string_array[i] = s

    print(fused_with_pointer(int_array))
    print()
    print(fused_with_pointer(long_array))
    print()
    print(fused_with_pointer(float_array))
    print()
    print(fused_with_pointer(string_array).decode('ascii'))

cdef fused_type1* fused_pointer_except_null(fused_type1* x) except NULL:
    if fused_type1 is string_t:
        assert(bool(x[0]))
    else:
        assert(x[0] < 10)
    return x

def test_fused_pointer_except_null(value):
    """
    >>> test_fused_pointer_except_null(1)
    1
    >>> test_fused_pointer_except_null(2.0)
    2.0
    >>> test_fused_pointer_except_null(b'foo')
    foo
    >>> test_fused_pointer_except_null(16)
    Traceback (most recent call last):
    AssertionError
    >>> test_fused_pointer_except_null(15.1)
    Traceback (most recent call last):
    AssertionError
    >>> test_fused_pointer_except_null(b'')
    Traceback (most recent call last):
    AssertionError
    """
    if isinstance(value, int):
        test_int = cython.declare(cython.int, value)
        print(fused_pointer_except_null(&test_int)[0])
    elif isinstance(value, float):
        test_float = cython.declare(cython.float, value)
        print(fused_pointer_except_null(&test_float)[0])
    elif isinstance(value, bytes):
        test_str = cython.declare(string_t, value)
        print(fused_pointer_except_null(&test_str)[0].decode('ascii'))

include "../testsupport/cythonarrayutil.pxi"

cpdef cython.integral test_fused_memoryviews(cython.integral[:, ::1] a):
    """
    >>> import cython
    >>> a = create_array((3, 5), mode="c")
    >>> test_fused_memoryviews[cython.int](a)
    7
    """
    return a[1, 2]

ctypedef int[:, ::1] memview_int
ctypedef long[:, ::1] memview_long
memview_t = cython.fused_type(memview_int, memview_long)

def test_fused_memoryview_def(memview_t a):
    """
    >>> a = create_array((3, 5), mode="c")
    >>> test_fused_memoryview_def["memview_int"](a)
    7
    """
    return a[1, 2]

cdef test_specialize(fused_type1 x, fused_type1 *y, composed_t z, other_t *a):
    cdef fused_type1 result

    if composed_t is p_double:
        print("double pointer")

    if fused_type1 in floating:
        result = x + y[0] + z[0] + a[0]
        return result

def test_specializations():
    """
    >>> test_specializations()
    double pointer
    double pointer
    double pointer
    double pointer
    double pointer
    """
    cdef object (*f)(double, double *, double *, int *)

    cdef double somedouble = 2.2
    cdef double otherdouble = 3.3
    cdef int someint = 4

    cdef p_double somedouble_p = &somedouble
    cdef p_double otherdouble_p = &otherdouble
    cdef p_int someint_p = &someint

    f = test_specialize
    assert f(1.1, somedouble_p, otherdouble_p, someint_p) == 10.6

    f = <object (*)(double, double *, double *, int *)> test_specialize
    assert f(1.1, somedouble_p, otherdouble_p, someint_p) == 10.6

    assert (<object (*)(double, double *, double *, int *)>
            test_specialize)(1.1, somedouble_p, otherdouble_p, someint_p) == 10.6

    f = test_specialize[double, int]
    assert f(1.1, somedouble_p, otherdouble_p, someint_p) == 10.6

    assert test_specialize[double, int](1.1, somedouble_p, otherdouble_p, someint_p) == 10.6

    # The following cases are not supported
    # f = test_specialize[double][p_int]
    # print f(1.1, somedouble_p, otherdouble_p)
    # print

    # print test_specialize[double][p_int](1.1, somedouble_p, otherdouble_p)
    # print

    # print test_specialize[double](1.1, somedouble_p, otherdouble_p)
    # print

cdef opt_args(integral x, floating y = 4.0):
    print(x, y)

def test_opt_args():
    """
    >>> test_opt_args()
    3 4.0
    3 4.0
    3 4.0
    3 4.0
    """
    opt_args[int,  float](3)
    opt_args[int, double](3)
    opt_args[int,  float](3, 4.0)
    opt_args[int, double](3, 4.0)

class NormalClass(object):
    def method(self, cython.integral i):
        print(cython.typeof(i), i)

def test_normal_class():
    """
    >>> test_normal_class()
    short 10
    """
    NormalClass().method[pure_cython.short](10)

def test_normal_class_refcount():
    """
    >>> test_normal_class_refcount()
    short 10
    0
    """
    import sys
    import gc
    x = NormalClass()
    c = sys.getrefcount(x)
    x.method[pure_cython.short](10)
    gc.collect()  # Limited API creates circular references inside CyFunction, so a GC collection is needed
    print(sys.getrefcount(x) - c)

def test_fused_declarations(cython.integral i, cython.floating f):
    """
    >>> test_fused_declarations[pure_cython.short, pure_cython.float](5, 6.6)
    short
    float
    25 43.56
    >>> test_fused_declarations[pure_cython.long, pure_cython.double](5, 6.6)
    long
    double
    25 43.56
    """
    cdef cython.integral squared_int = i * i
    cdef cython.floating squared_float = f * f

    assert cython.typeof(squared_int) == cython.typeof(i)
    assert cython.typeof(squared_float) == cython.typeof(f)

    print(cython.typeof(squared_int))
    print(cython.typeof(squared_float))
    print('%d %.2f' % (squared_int, squared_float))

def test_sizeof_fused_type(fused_type1 b):
    """
    >>> test_sizeof_fused_type[pure_cython.double](11.1)
    """
    t = sizeof(b), sizeof(fused_type1), sizeof(double)
    assert t[0] == t[1] == t[2], t

def get_array(itemsize, format):
    result = array((10,), itemsize, format)
    result[5] = 5.0
    result[6] = 6.0
    return result

def get_intc_array():
    result = array((10,), sizeof(int), 'i')
    result[5] = 5
    result[6] = 6
    return result

def test_fused_memslice_dtype(cython.floating[:] array):
    """
    Note: the np.ndarray dtype test is in numpy_test

    >>> import cython
    >>> sorted(test_fused_memslice_dtype.__signatures__)
    ['double', 'float']

    >>> test_fused_memslice_dtype[cython.double](get_array(8, 'd'))
    double[:] double[:] 5.0 6.0
    >>> test_fused_memslice_dtype[cython.float](get_array(4, 'f'))
    float[:] float[:] 5.0 6.0

    # None should evaluate to *something* (currently the first
    # in the list, but this shouldn't be a hard requirement)
    >>> test_fused_memslice_dtype(None)
    float[:]
    >>> test_fused_memslice_dtype[cython.double](None)
    double[:]
    """
    if array is None:
        print(cython.typeof(array))
        return
    cdef cython.floating[:] otherarray = array[0:100:1]
    print(cython.typeof(array), cython.typeof(otherarray),
          array[5], otherarray[6])
    cdef cython.floating value;
    cdef cython.floating[:] test_cast = <cython.floating[:1:1]>&value

def test_fused_memslice_dtype_repeated(cython.floating[:] array1, cython.floating[:] array2):
    """
    Note: the np.ndarray dtype test is in numpy_test

    >>> sorted(test_fused_memslice_dtype_repeated.__signatures__)
    ['double', 'float']

    >>> test_fused_memslice_dtype_repeated(get_array(8, 'd'), get_array(8, 'd'))
    double[:] double[:]
    >>> test_fused_memslice_dtype_repeated(get_array(4, 'f'), get_array(4, 'f'))
    float[:] float[:]
    >>> test_fused_memslice_dtype_repeated(get_array(8, 'd'), get_array(4, 'f'))
    Traceback (most recent call last):
    ValueError: Buffer dtype mismatch, expected 'double' but got 'float'
    """
    print(cython.typeof(array1), cython.typeof(array2))

def test_fused_memslice_dtype_repeated_2(cython.floating[:] array1, cython.floating[:] array2,
                                         fused_type3[:] array3):
    """
    Note: the np.ndarray dtype test is in numpy_test

    >>> sorted(test_fused_memslice_dtype_repeated_2.__signatures__)
    ['double|double', 'double|int', 'float|double', 'float|int']

    >>> test_fused_memslice_dtype_repeated_2(get_array(8, 'd'), get_array(8, 'd'), get_array(8, 'd'))
    double[:] double[:] double[:]
    >>> test_fused_memslice_dtype_repeated_2(get_array(8, 'd'), get_array(8, 'd'), get_intc_array())
    double[:] double[:] int[:]
    >>> test_fused_memslice_dtype_repeated_2(get_array(4, 'f'), get_array(4, 'f'), get_intc_array())
    float[:] float[:] int[:]
    """
    print(cython.typeof(array1), cython.typeof(array2), cython.typeof(array3))

def test_fused_const_memslice_dtype_repeated(const cython.floating[:] array1, cython.floating[:] array2):
    """Test fused types memory view with one being const

    >>> sorted(test_fused_const_memslice_dtype_repeated.__signatures__)
    ['double', 'float']

    >>> test_fused_const_memslice_dtype_repeated(get_array(8, 'd'), get_array(8, 'd'))
    const double[:] double[:]
    >>> test_fused_const_memslice_dtype_repeated(get_array(4, 'f'), get_array(4, 'f'))
    const float[:] float[:]
    >>> test_fused_const_memslice_dtype_repeated(get_array(8, 'd'), get_array(4, 'f'))
    Traceback (most recent call last):
    ValueError: Buffer dtype mismatch, expected 'double' but got 'float'
    """
    print(cython.typeof(array1), cython.typeof(array2))

def test_cython_numeric(cython.numeric arg):
    """
    Test to see whether complex numbers have their utility code declared
    properly.

    >>> test_cython_numeric(10.0 + 1j)
    double complex (10+1j)
    """
    print(cython.typeof(arg), arg)


cdef fused int_t:
    int

def test_pylong(int_t i):
    """
    >>> import cython
    >>> try:    long = long # Python 2
    ... except: long = int  # Python 3

    >>> test_pylong[int](int(0))
    int
    >>> test_pylong[cython.int](int(0))
    int
    >>> test_pylong(int(0))
    int

    >>> test_pylong[int](long(0))
    int
    >>> test_pylong[cython.int](long(0))
    int
    >>> test_pylong(long(0))
    int

    >>> test_pylong[cython.long](0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    KeyError: ...
    """
    print(cython.typeof(i))


cdef fused ints_t:
    int
    long

cdef _test_index_fused_args(cython.floating f, ints_t i):
    print(cython.typeof(f), cython.typeof(i))

def test_index_fused_args(cython.floating f, ints_t i):
    """
    >>> import cython
    >>> test_index_fused_args[cython.double, cython.int](2.0, 3)
    double int
    """
    _test_index_fused_args[cython.floating, ints_t](f, i)

cdef _test_index_const_fused_args(const cython.floating f, const ints_t i):
    print((cython.typeof(f), cython.typeof(i)))

def test_index_const_fused_args(const cython.floating f, const ints_t i):
    """Test indexing function implementation with const fused type args

    >>> import cython
    >>> test_index_const_fused_args[cython.double, cython.int](2.0, 3)
    ('const double', 'const int')
    """
    _test_index_const_fused_args[cython.floating, ints_t](f, i)


def test_composite(fused_composite x):
    """
    >>> print(test_composite(b'a').decode('ascii'))
    a
    >>> test_composite(3)
    6
    >>> test_composite(3.0)
    6.0
    """
    if fused_composite is string_t:
        return x
    else:
        return 2 * x


cdef cdef_func_const_fused_arg(const cython.floating val,
                               const fused_type1 * ptr_to_const,
                               const (cython.floating *) const_ptr):
    print((val, cython.typeof(val)))
    print((ptr_to_const[0], cython.typeof(ptr_to_const[0])))
    print((const_ptr[0], cython.typeof(const_ptr[0])))

    ptr_to_const = NULL  # pointer is not const, value is const
    const_ptr[0] = 0.0  # pointer is const, value is not const

def test_cdef_func_with_const_fused_arg():
    """Test cdef function with const fused type argument

    >>> test_cdef_func_with_const_fused_arg()
    (0.0, 'const float')
    (1, 'const int')
    (2.0, 'float')
    """
    cdef float arg0 = 0.0
    cdef int arg1 = 1
    cdef float arg2 = 2.0
    cdef_func_const_fused_arg(arg0, &arg1, &arg2)


cdef in_check_1(just_float x):
    return just_float in floating

cdef in_check_2(just_float x, floating y):
    # the "floating" on the right-hand side of the in statement should not be specialized
    # - the test should still work.
    return just_float in floating

cdef in_check_3(floating x):
    # the floating on the left-hand side of the in statement should be specialized
    # but the one of the right-hand side should not (so that the test can still work).
    return floating in floating

def test_fused_in_check():
    """
    It should be possible to use fused types on in "x in ...fused_type" statements
    even if that type is specialized in the function.

    >>> test_fused_in_check()
    True
    True
    True
    True
    """
    print(in_check_1(1.0))
    print(in_check_2(1.0, 2.0))
    print(in_check_2[float, double](1.0, 2.0))
    print(in_check_3[float](1.0))


### see GH3642 - presence of cdef inside "unrelated" caused a type to be incorrectly inferred
cdef unrelated(cython.floating x):
    cdef cython.floating t = 1
    return t

cdef handle_float(float* x): return 'float'

cdef handle_double(double* x): return 'double'

def convert_to_ptr(cython.floating x):
    """
    >>> convert_to_ptr(1.0)
    'double'
    >>> convert_to_ptr['double'](1.0)
    'double'
    >>> convert_to_ptr['float'](1.0)
    'float'
    """
    if cython.floating is float:
        return handle_float(&x)
    elif cython.floating is double:
        return handle_double(&x)

def constfused_with_typedef(const fused_with_typedef[:] x):
    """
    >>> constfused_with_typedef(get_array(8, 'd'))
    5.0
    >>> constfused_with_typedef(get_intc_array())
    5
    """
    return x[5]

def constfused_typedef_name_clashes(const fused_with_typedef[:] x, fused_misleading_name[:] y):
    """
    This'll deliberately end up with two typedefs that generate the same name in dispatch code
    (and thus one needs to end up numbered to make it work).
    It's mainly a compile test and the runtime part is fairly token.

    >>> constfused_typedef_name_clashes(get_intc_array(), get_array(4, 'f'))
    (5, 5.0)
    """
    return x[5], y[5]

cdef double get_double():
    return 1.0
cdef float get_float():
    return 0.0

cdef call_func_pointer(cython.floating (*f)()):
    return f()

def test_fused_func_pointer():
    """
    >>> test_fused_func_pointer()
    1.0
    0.0
    """
    print(call_func_pointer(get_double))
    print(call_func_pointer(get_float))

cdef double get_double_from_int(int i):
    return i

cdef call_func_pointer_with_1(cython.floating (*f)(cython.integral)):
    return f(1)

def test_fused_func_pointer2():
    """
    >>> test_fused_func_pointer2()
    1.0
    """
    print(call_func_pointer_with_1(get_double_from_int))

cdef call_function_that_calls_fused_pointer(object (*f)(cython.floating (*)(cython.integral))):
    if cython.floating is double and cython.integral is int:
        return 5*f(get_double_from_int)
    else:
        return None  # practically it's hard to make this kind of function useful...

def test_fused_func_pointer_multilevel():
    """
    >>> test_fused_func_pointer_multilevel()
    5.0
    None
    """
    print(call_function_that_calls_fused_pointer(call_func_pointer_with_1[double, int]))
    print(call_function_that_calls_fused_pointer(call_func_pointer_with_1[float, int]))

cdef null_default(cython.floating x, cython.floating *x_minus_1_out=NULL):
    # On C++ a void* can't be assigned to a regular pointer, therefore setting up
    # needs to avoid going through a void* temp
    if x_minus_1_out:
        x_minus_1_out[0] = x-1
    return x

def test_null_default():
    """
    >>> test_null_default()
    2.0 1.0
    2.0
    2.0 1.0
    2.0
    """
    cdef double xd = 2.
    cdef double xd_minus_1
    result = null_default(xd, &xd_minus_1)
    print(result, xd_minus_1)
    result = null_default(xd)
    print(result)

    cdef float xf = 2.
    cdef float xf_minus_1
    result = null_default(xf, &xf_minus_1)
    print(result, xf_minus_1)
    result = null_default(xf)
    print(result)


cdef cython.numeric fused_numeric_default(int a = 1, cython.numeric x = 0):
    return x + a

def test_fused_numeric_default(int a, x):
    """
    >>> test_fused_numeric_default(1, 0)
    [1, 1.0, (1+0j)]

    >>> test_fused_numeric_default(1, 2)
    [3, 3.0, (3+0j)]

    >>> test_fused_numeric_default(2, 0)
    [2, 2.0, (2+0j)]

    >>> test_fused_numeric_default(2, 1)
    [3, 3.0, (3+0j)]
    """
    result = []

    if a == 1 and x == 0:
        result.append(fused_numeric_default[int]())
    elif x == 0:
        result.append(fused_numeric_default[int](a))
    elif a == 1:
        result.append(fused_numeric_default[int](1, x))
    else:
        result.append(fused_numeric_default[int](a, x))

    if a == 1 and x == 0:
        result.append(fused_numeric_default[float]())
    elif x == 0:
        result.append(fused_numeric_default[float](a))
    elif a == 1:
        result.append(fused_numeric_default[float](1, x))
    else:
        result.append(fused_numeric_default[float](a, x))

    if a == 1 and x == 0:
        result.append(fused_numeric_default[cython.doublecomplex]())
    elif x == 0:
        result.append(fused_numeric_default[cython.doublecomplex](a))
    elif a == 1:
        result.append(fused_numeric_default[cython.doublecomplex](1, x))
    else:
        result.append(fused_numeric_default[cython.doublecomplex](a, x))

    return result
