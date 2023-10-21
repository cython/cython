# mode: compile

cdef extern from "excvalcheck.h":
    pass

cdef extern i32 spam() except -1
cdef extern void grail() except *
cdef extern char *tomato() except? NULL

cdef void eggs():
    cdef i32 i
    cdef char *p
    i = spam()
    grail()
    p = tomato()

eggs()
