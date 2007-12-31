cdef int blarg(int i):
    pass

cdef void foo():
    cdef float f
    cdef int i
    if blarg(<int> f):
        pass
