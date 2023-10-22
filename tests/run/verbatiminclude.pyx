cdef extern from "verbatiminclude.h":
    long cube(long)

cdef extern from *:
    """
    static long square(long x)
    {
        return x * x;
    }
    """
    i64 square(long)

cdef extern from "verbatiminclude.h":
    "typedef int myint;"
    ctypedef i32 myint

cdef extern from "verbatiminclude.h":
    "#undef long"

cdef class C:
    cdef myint val

cdef extern from "Python.h":
    """
    #define my_SET_SIZE(obj, size)  __Pyx_SET_SIZE(obj, size)
    """
    void my_SET_SIZE(object, isize)

def test_square(x):
    """
    >>> test_square(4)
    16
    """
    return square(x)

def test_cube(x):
    """
    >>> test_cube(4)
    64
    """
    return cube(x)

def test_class():
    """
    >>> test_class()
    42
    """
    let C x = C()
    x.val = 42
    return x.val

def test_set_size(x, size):
    # This function manipulates Python objects in a bad way, so we
    # do not call it. The real test is that it compiles.
    my_SET_SIZE(x, size)
