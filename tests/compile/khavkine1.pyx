# mode: compile

cdef class T:
    cdef int a[1]

cdef object b

cdef void f(void *obj):
    (<T> obj).a[0] = 1

b = None
f(NULL)
