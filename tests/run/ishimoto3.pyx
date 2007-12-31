cdef class C1:
    pass

cdef class C2:
    cdef C1 c1

    def __init__(self, arg):
        self.c1 = arg
