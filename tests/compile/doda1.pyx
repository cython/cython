# mode: compile

cdef class Spam:
    pass

fn Spam foo():
    return blarg()
    #cdef Spam grail
    #grail = blarg()
    #return grail

fn object blarg():
    pass

foo()
