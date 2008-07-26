cdef class Spam:
    pass

cdef int f() except -1:
    cdef type t
    t = Spam
