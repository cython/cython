# mode: compile

cdef char *p1
cdef int *p2
cdef int x

p1 = NULL
p2 = NULL
x = p1 == NULL
x = NULL == p2
