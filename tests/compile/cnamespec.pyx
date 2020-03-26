# mode: compile

cdef extern from *:
    """
    int c_a, c_b;
    """
    int a "c_a", b "c_b"

cdef struct foo "c_foo":
    int i "c_i"

ctypedef enum blarg "c_blarg":
    x "c_x"
    y "c_y" = 42

cdef double spam "c_spam" (int i, float f):
    cdef double d "c_d"
    cdef foo *p
    global b
    if i:
      d = spam(a, f)
    cdef foo q
    q.i = 7
    p = &q
    b = p.i
    p.i = x
    p.i = y

cdef inline double spam2 "c_spam2" (int i, float f):
    return spam(i,f)
