cdef int i
cdef x

def f(a):
    global i, x
    i = 42
    x = a
