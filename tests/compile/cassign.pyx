# mode: compile

cdef void foo():
    cdef int i1, i2=0
    cdef char c1=0, c2
    cdef char *p1, *p2=NULL
    cdef object obj1
    i1 = i2
    i1 = c1
    p1 = p2
    obj1 = i1
    i1 = obj1
    p1 = obj1
    p1 = "spanish inquisition"

foo()
