# mode: compile

cdef extern from "excvalcheck.h":
    pass

cdef extern int spam() except -1
cdef extern void grail() except *
cdef extern char *tomato() except? NULL

cdef void eggs():
    cdef int i
    cdef char *p
    i = spam()
    grail()
    p = tomato()

eggs()
