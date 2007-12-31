cdef class Grail:

    def __add__(int x, float y):
        pass
    
    def __getslice__(self, i, j):
        pass

    def __setslice__(self, Py_ssize_t i, float j, x):
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

