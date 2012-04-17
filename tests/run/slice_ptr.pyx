from libc.stdlib cimport malloc, free
from cpython.object cimport Py_EQ, Py_NE

def double_ptr_slice(x, L, int a, int b):
    """
    >>> L = list(range(10))
    >>> double_ptr_slice(5, L, 0, 10)
    >>> double_ptr_slice(6, L, 0, 10)
    >>> double_ptr_slice(None, L, 0, 10)
    >>> double_ptr_slice(0, L, 3, 7)
    >>> double_ptr_slice(5, L, 3, 7)
    >>> double_ptr_slice(9, L, 3, 7)

    >>> double_ptr_slice(EqualsEvens(), L, 0, 10)
    >>> double_ptr_slice(EqualsEvens(), L, 1, 10)
    """
    cdef double *L_c = NULL
    try:
        L_c = <double*>malloc(len(L) * sizeof(double))
        for i, a in enumerate(L):
            L_c[i] = L[i]
        assert (x in L_c[:b]) == (x in L[:b])
        assert (x not in L_c[:b]) == (x not in L[:b])
        assert (x in L_c[a:b]) == (x in L[a:b])
        assert (x not in L_c[a:b]) == (x not in L[a:b])
        assert (x in L_c[a:b:2]) == (x in L[a:b:2])
        assert (x not in L_c[a:b:2]) == (x not in L[a:b:2])
    finally:
        free(L_c)

def void_ptr_slice(py_x, L, int a, int b):
    """
    >>> L = list(range(10))
    >>> void_ptr_slice(5, L, 0, 10)
    >>> void_ptr_slice(6, L, 0, 10)
    >>> void_ptr_slice(None, L, 0, 10)
    >>> void_ptr_slice(0, L, 3, 7)
    >>> void_ptr_slice(5, L, 3, 7)
    >>> void_ptr_slice(9, L, 3, 7)
    """
    # I'm using the fact that small Python ints are cached.
    cdef void **L_c = NULL
    cdef void *x = <void*>py_x
    try:
        L_c = <void**>malloc(len(L) * sizeof(void*))
        for i, a in enumerate(L):
            L_c[i] = <void*>L[i]
        assert (x in L_c[:b]) == (py_x in L[:b])
        assert (x not in L_c[:b]) == (py_x not in L[:b])
        assert (x in L_c[a:b]) == (py_x in L[a:b])
        assert (x not in L_c[a:b]) == (py_x not in L[a:b])
        assert (x in L_c[a:b:2]) == (py_x in L[a:b:2])
        assert (x not in L_c[a:b:2]) == (py_x not in L[a:b:2])
    finally:
        free(L_c)

cdef class EqualsEvens:
    """
    >>> e = EqualsEvens()
    >>> e == 2
    True
    >>> e == 5
    False
    >>> [e == k for k in range(4)]
    [True, False, True, False]
    """
    def __richcmp__(self, other, int op):
        if op == Py_EQ:
            return other % 2 == 0
        elif op == Py_NE:
            return other % 2 == 1
        else:
            return False
