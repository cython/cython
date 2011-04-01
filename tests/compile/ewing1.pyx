# mode: compile

cdef int blarg(int i):
    pass

cdef void foo():
    cdef float f=0
    cdef int i
    if blarg(<int> f):
        pass

foo()
