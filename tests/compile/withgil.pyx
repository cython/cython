cdef void f() with gil:
    x = 42

cdef object g(object x) with gil:
    pass
