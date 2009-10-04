__doc__ = u"""
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
    
    >>> expression()
    double
    double complex
    int
    unsigned int
"""

from cython cimport typeof

cdef class A:
    pass

cdef class B(A):
    pass

cdef struct X:
    double a
    double complex b

def simple():
    cdef int i
    cdef long l
    cdef long long ll
    cdef int* iptr
    cdef int** iptrptr
    cdef A a
    cdef B b
    cdef X x
    print typeof(i)
    print typeof(l)
    print typeof(ll)
    print typeof(iptr)
    print typeof(iptrptr)
    print typeof(a)
    print typeof(b)
    print typeof(x)
    print typeof(None)
    
def expression():
    cdef X x
    cdef X *xptr
    cdef short s
    cdef int i
    cdef unsigned int ui
    print typeof(x.a)
    print typeof(xptr.b)
    print typeof(s + i)
    print typeof(i + ui)
