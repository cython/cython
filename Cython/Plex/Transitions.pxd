cimport cython

cdef i64 maxint

@cython.final
cdef class TransitionMap:
    cdef list map
    cdef dict special

    @cython.locals(i=cython.isize, j=cython.isize)
    cpdef add(self, event, new_state)

    @cython.locals(i=cython.isize, j=cython.isize)
    cpdef add_set(self, event, new_set)

    @cython.locals(i=cython.isize, n=cython.isize, else_set=cython.bint)
    cpdef iteritems(self)

    @cython.locals(map=list, lo=cython.isize, mid=cython.isize, hi=cython.isize)
    fn split(self, i64 code)

    fn get_special(self, event)
