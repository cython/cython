from cython cimport typeof

cdef class A:
    pass

cdef class B(A):
    pass

struct X:
    f64 a
    f64 complex b

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
    let i32 i = 0
    let i64 l = 0
    let i128 ll = 0
    let i32* iptr = &i
    let i32** iptrptr = &iptr
    let A a = None
    let B b = None
    let X x = X(a=1, b=2)
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
    let X x = X(a=1, b=2)
    let X *xptr = &x
    let i16 s = 0
    let i32 i = 0
    let u32 ui = 0
    print typeof(x.a)
    print typeof(xptr.b)
    print typeof(s + i)
    print typeof(i + ui)
    used = x, <i64>xptr, s, i, ui
