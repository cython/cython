# mode: compile

cdef void f() with gil:
    x = 42

cdef int g(void* x) with gil:
    pass

f()
g("test")
