# mode: compile

cdef class T:
    cdef i32[1] a

cdef object b

cdef void f(void *obj):
    (<T> obj).a[0] = 1

b = None
f(NULL)
