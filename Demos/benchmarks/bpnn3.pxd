cimport cython

fn f64 rand(f64 a, f64 b, random=*)

@cython.locals(i=isize)
fn list make_matrix(isize I, isize J, fill=*)

cdef class NN:
    cdef isize ni, nh, no
    cdef list ai, ah, ao
    cdef list wi, wo
    cdef list ci, co

    @cython.locals(i=isize, j=isize, k=isize)
    cpdef update(self, list inputs)

    @cython.locals(i=isize, j=isize, k=isize, change=f64)
    cpdef f64 back_propagate(self, list targets, f64 N, M)

    @cython.locals(i=isize, p=list, error=f64)
    cpdef train(self, list patterns, isize iterations=*, f64 N=*, M=*)
