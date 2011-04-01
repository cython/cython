# mode: compile

ctypedef union pet:
    int cat
    float dog

cdef pet sam

sam.cat = 1
sam.dog = 2.7

