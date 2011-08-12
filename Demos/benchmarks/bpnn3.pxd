cimport cython

cdef double rand(double a, double b, random=*)

@cython.locals(i=Py_ssize_t)
cdef list makeMatrix(Py_ssize_t I, Py_ssize_t J, fill=*)

cdef class NN:
    cdef Py_ssize_t ni, nh, no
    cdef list ai, ah, ao
    cdef list wi, wo
    cdef list ci, co

    @cython.locals(i=Py_ssize_t, j=Py_ssize_t, k=Py_ssize_t)
    cpdef update(self, list inputs)

    @cython.locals(i=Py_ssize_t, j=Py_ssize_t, k=Py_ssize_t, change=double)
    cpdef double backPropagate(self, list targets, double N, M)

    @cython.locals(i=Py_ssize_t, p=list, error=double)
    cpdef train(self, list patterns, Py_ssize_t iterations=*, double N=*, M=*)
