# mode: compile

cdef void f():
    cdef u64 x
    cdef object y=0
    x = y
    y = x

f()
