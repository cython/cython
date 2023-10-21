# mode: compile

cdef extern from *:
    """
    int c_a, c_b;
    """
    i32 a "c_a", b "c_b"

cdef struct foo "c_foo":
    i32 i "c_i"

ctypedef enum blarg "c_blarg":
    x "c_x"
    y "c_y" = 42

cdef f64 spam "c_spam" (i32 i, f32 f):
    cdef f64 d "c_d"
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

cdef inline f64 spam2 "c_spam2" (i32 i, f32 f):
    return spam(i,f)
