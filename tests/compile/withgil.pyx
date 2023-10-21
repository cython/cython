# mode: compile

cdef void f() with gil:
    x = 42

cdef i32 g(void* x) with gil:
    pass

f()
g("test")
