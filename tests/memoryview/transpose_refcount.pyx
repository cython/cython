# mode: run

from cython cimport view

cdef bint print_upper_right(double[:, :] M):
    print M[0, 1]

cdef class MemViewContainer:
    cdef double[:, :] A

    def __init__(self, A):
        self.A = A

    cpdef run(self):
        print_upper_right(self.A)
        print_upper_right(self.A.T)
        print_upper_right(self.A.T)

def test_transpose_refcount():
    """
    >>> test_transpose_refcount()
    2.0
    3.0
    3.0
    """
    cdef double[:, :] A = view.array(shape=(2, 2), itemsize=sizeof(double), format="d")
    A[0, 0], A[0, 1], A[1, 0], A[1, 1] = 1., 2., 3., 4.
    cdef MemViewContainer container = MemViewContainer(A)
    container.run()
