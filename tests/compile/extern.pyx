# mode: compile

cdef extern int i
cdef extern char *s[]
cdef extern void spam(char c)

cdef extern int eggs():
    pass

cdef int grail():
    pass

grail()
