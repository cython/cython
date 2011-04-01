# mode: compile

cdef enum Color:
    red
    white
    blue

cdef void f():
    cdef Color e
    cdef int i

    i = red
    i = red + 1
    i = red | 1
    e = white
    i = e
    i = e + 1

f()
