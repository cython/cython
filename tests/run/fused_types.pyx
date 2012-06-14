# mode: run

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


def test_pure():
    """
    >>> test_pure()
    10
    """
    mytype = pure_cython.typedef(pure_cython.fused_type(int, long, complex))
    print mytype(10)


cdef cdef_func_with_fused_args(fused_type1 x, fused_type1 y, fused_type2 z):
    if fused_type1 is string_t:
        print x.decode('ascii'), y.decode('ascii'), z.decode('ascii')
    else:
        print x, y, z.decode('ascii')

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
    print cdef_func_with_fused_args(b'spam', b'ham', b'eggs').decode('ascii')
    print cdef_func_with_fused_args(10, 20, b'butter')
    print cdef_func_with_fused_args(4.2, 8.6, b'bunny')

cdef fused_type1 fused_with_pointer(fused_type1 *array):
    for i in range(5):
        if fused_type1 is string_t:
            print array[i].decode('ascii')
        else:
            print array[i]

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
    cdef int int_array[5]
    cdef long long_array[5]
    cdef float float_array[5]
    cdef string_t string_array[5]

    cdef char *s

    strings = [b"humpty", b"dumpty", b"fall", b"splatch", b"breakfast"]

    for i in range(5):
        int_array[i] = i
        long_array[i] = i
        float_array[i] = i
        s = strings[i]
        string_array[i] = s

    print fused_with_pointer(int_array)
    print
    print fused_with_pointer(long_array)
    print
    print fused_with_pointer(float_array)
    print
    print fused_with_pointer(string_array).decode('ascii')

include "cythonarrayutil.pxi"

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
        print "double pointer"

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
    print x, y

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
        print cython.typeof(i), i

def test_normal_class():
    """
    >>> test_normal_class()
    short 10
    """
    NormalClass().method[pure_cython.short](10)

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

    print cython.typeof(squared_int)
    print cython.typeof(squared_float)
    print '%d %.2f' % (squared_int, squared_float)

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
    """
    cdef cython.floating[:] otherarray = array[0:100:1]
    print cython.typeof(array), cython.typeof(otherarray), \
          array[5], otherarray[6]

def test_cython_numeric(cython.numeric arg):
    """
    Test to see whether complex numbers have their utility code declared
    properly.

    >>> test_cython_numeric(10.0 + 1j)
    double complex (10+1j)
    """
    print cython.typeof(arg), arg

cdef fused ints_t:
    int
    long

cdef _test_index_fused_args(cython.floating f, ints_t i):
    print cython.typeof(f), cython.typeof(i)

def test_index_fused_args(cython.floating f, ints_t i):
    """
    >>> import cython
    >>> test_index_fused_args[cython.double, cython.int](2.0, 3)
    double int
    """
    _test_index_fused_args[cython.floating, ints_t](f, i)
