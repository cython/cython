cdef class Grail:

    def __add__(int x, float y):
        pass

cdef class Swallow:
    pass
    
def f(Grail g):
    cdef int i
    cdef Swallow s
    g = x
    x = g
    g = i
    i = g
    g = s
    s = g

