# mode: compile

cdef char *p1
cdef i32 *p2
cdef i32 x

p1 = NULL
p2 = NULL
x = p1 == NULL
x = NULL == p2
