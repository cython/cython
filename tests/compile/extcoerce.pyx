# mode: compile

cdef class Grail:

    def __add__(i32 x, f32 y):
        pass

cdef class Swallow:
    pass

def f(Grail g):
    cdef i32 i = 0
    cdef Swallow s = Swallow()
    cdef object x = Grail()
    g = x
    x = g
    g = i
    i = g
    g = s
    s = g
