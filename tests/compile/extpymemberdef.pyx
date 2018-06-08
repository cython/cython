# mode: compile

cdef class Spam:
    cdef public char c
    cdef public int i
    cdef public long l
    cdef public unsigned char uc
    cdef public unsigned int ui
    cdef public unsigned long ul
    cdef public float f
    cdef public double d
    cdef public char *s
    cdef readonly char[42] a
    cdef public object o
    cdef readonly int r
    cdef readonly Spam e
