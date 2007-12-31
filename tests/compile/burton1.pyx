cdef void f():
    cdef void (*p)()
    p = <void(*)()>0
    (<int (*)()>p)()
