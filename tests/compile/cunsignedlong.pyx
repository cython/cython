# mode: compile

cdef void f():
    cdef unsigned long x
    cdef object y=0
    x = y
    y = x

f()
