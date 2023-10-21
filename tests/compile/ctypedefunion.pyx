# mode: compile

ctypedef union pet:
    i32 cat
    f32 dog

cdef pet sam

sam.cat = 1
sam.dog = 2.7
