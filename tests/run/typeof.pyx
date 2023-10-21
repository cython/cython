from cython cimport typeof

cdef class A:
    pass

cdef class B(A):
    pass

cdef struct X:
    f64 a
    double complex b

def simple():
    """
    >>> simple()
    int
    long
    long long
    int *
    int **
    A
    B
    X
    Python object
    """
    cdef i32 i = 0
    cdef i64 l = 0
    cdef i128 ll = 0
    cdef i32* iptr = &i
    cdef i32** iptrptr = &iptr
    cdef A a = None
    cdef B b = None
    cdef X x = X(a=1, b=2)
    print typeof(i)
    print typeof(l)
    print typeof(ll)
    print typeof(iptr)
    print typeof(iptrptr)
    print typeof(a)
    print typeof(b)
    print typeof(x)
    print typeof(None)
    used = i, l, ll, <i64>iptr, <i64>iptrptr, a, b, x

def expression():
    """
    >>> expression()
    double
    double complex
    int
    unsigned int
    """
    cdef X x = X(a=1, b=2)
    cdef X *xptr = &x
    cdef i16 s = 0
    cdef i32 i = 0
    cdef u32 ui = 0
    print typeof(x.a)
    print typeof(xptr.b)
    print typeof(s + i)
    print typeof(i + ui)
    used = x, <i64>xptr, s, i, ui
