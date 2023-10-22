# mode: compile

cdef enum Color:
    red
    white
    blue

cdef void f():
    let Color e
    let i32 i

    i = red
    i = red + 1
    i = red | 1
    e = white
    i = e
    i = e + 1

f()
