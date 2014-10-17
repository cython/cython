
cdef int wrong_args(int x, long y)

cdef long wrong_return_type(int x, int y)

cdef int wrong_exception_check(int x, int y) except 0

cdef int wrong_exception_value(int x, int y) except 0

cdef int wrong_exception_value_check(int x, int y) except 0

cdef int inherit_exception_value(int x, int y) except 0

cdef int inherit_exception_check(int x, int y) except *
