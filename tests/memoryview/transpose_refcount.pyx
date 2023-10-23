# mode: run

from cython cimport view

fn bint print_upper_right(f64[:, :] M):
    print M[0, 1]

cdef class MemViewContainer:
    let f64[:, :] A

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
    let f64[:, :] A = view.array(shape=(2, 2), itemsize=sizeof(f64), format="d")
    A[0, 0], A[0, 1], A[1, 0], A[1, 1] = 1., 2., 3., 4.
    let MemViewContainer container = MemViewContainer(A)
    container.run()
