cimport cython

@cython.locals(egg=double)
cdef foo(egg)

@cython.locals(egg=cython.double)
cdef foo_defval(egg=*)

@cython.locals(egg=cython.bint, v=cython.int)
cpdef cpfoo(egg=*)
