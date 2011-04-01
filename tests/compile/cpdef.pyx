# mode: compile

cdef class A:
    cpdef a(self):
        ma(self)

cpdef ma(x):
    print x
