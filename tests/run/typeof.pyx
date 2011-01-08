from cython cimport typeof

cdef class A:
    pass

cdef class B(A):
    pass

cdef struct X:
    double a
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
    cdef int i = 0
    cdef long l = 0
    cdef long long ll = 0
    cdef int* iptr = &i
    cdef int** iptrptr = &iptr
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
    used = i, l, ll, <long>iptr, <long>iptrptr, a, b, x

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
    cdef short s = 0
    cdef int i = 0
    cdef unsigned int ui = 0
    print typeof(x.a)
    print typeof(xptr.b)
    print typeof(s + i)
    print typeof(i + ui)
    used = x, <long>xptr, s, i, ui
