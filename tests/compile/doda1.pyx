# mode: compile

cdef class Spam:
    pass

cdef Spam foo():
    return blarg()
    #cdef Spam grail
    #grail = blarg()
    #return grail

cdef object blarg():
    pass

foo()
