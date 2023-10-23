# mode: compile

extern from "excvalcheck.h":
    pass

cdef extern i32 spam() except -1
cdef extern void grail() except *
cdef extern char *tomato() except? NULL

fn void eggs():
    let i32 i
    let char *p
    i = spam()
    grail()
    p = tomato()

eggs()
