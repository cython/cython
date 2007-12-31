DEF NO = 0
DEF YES = 1

cdef void f():
    cdef int i
    IF YES:
        i = 1
    ELIF NO:
        i = 2
    ELSE:
        i = 3

cdef void g():
    cdef int i
    IF NO:
        i = 1
    ELIF YES:
        i = 2
    ELSE:
        i = 3

cdef void h():
    cdef int i
    IF NO:
        i = 1
    ELIF NO:
        i = 2
    ELSE:
        i = 3
