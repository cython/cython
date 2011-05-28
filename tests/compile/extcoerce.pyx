# mode: compile

cdef class Grail:

    def __add__(int x, float y):
        pass

cdef class Swallow:
    pass

def f(Grail g):
    cdef int i = 0
    cdef Swallow s = Swallow()
    cdef object x = Grail()
    g = x
    x = g
    g = i
    i = g
    g = s
    s = g

